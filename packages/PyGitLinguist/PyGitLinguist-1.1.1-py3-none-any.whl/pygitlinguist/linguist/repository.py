import os
import tempfile
import shutil
from git import Repo
from linguist.language import Language


class LazyBlob:
    GIT_ATTR = ['linguist-documentation',
                'linguist-language',
                'linguist-vendored',
                'linguist-generated',
                'linguist-detectable']

    MAX_SIZE = 128 * 1024

    def __init__(self, repo, oid, path, mode=None):
        self.repository = repo
        self.oid = oid
        self.path = path
        self.mode = mode
        self._data = None
        self._git_attributes = None
        self._language = None

    @property
    def name(self):
        return self.path

    @property
    def git_attributes(self):
        if self._git_attributes is None:
            config_parser = self.repository.config_reader()
            section_name = "attr " + self.name
            self._git_attributes = dict(config_parser.items(section_name))
        return self._git_attributes

    def documentation(self):
        attribute = self.git_attributes.get('linguist-documentation')
        if attribute is not None:
            return self.boolean_attribute(attribute)
        return super().documentation()

    def generated(self):
        attribute = self.git_attributes.get('linguist-generated')
        if attribute is not None:
            return self.boolean_attribute(attribute)
        return super().generated()

    def vendored(self):
        attribute = self.git_attributes.get('linguist-vendored')
        if attribute is not None:
            return self.boolean_attribute(attribute)
        return super().vendored()

    def language(self):
        if self._language is not None:
            return self._language

        lang = self.git_attributes.get('linguist-language')
        if lang:
            self._language = Language.find_by_alias(lang)
        else:
            self._language = super().language()
        return self._language

    def detectable(self):
        attribute = self.git_attributes.get('linguist-detectable')
        if attribute is not None:
            return self.boolean_attribute(attribute)
        return None

    def data(self):
        self.load_blob()
        return self._data

    def size(self):
        self.load_blob()
        return self._size

    def symlink(self):
        return False  # We don't create LazyBlobs for symlinks.

    def cleanup(self):
        if self._data:
            self._data.clear()

    @staticmethod
    def boolean_attribute(attribute):
        return attribute != "false" and attribute is not False

    def load_blob(self):
        if self._data is None:
            repo = self.repository
            commit = repo.commit(self.oid)
            blob = commit.tree / self.name
            self._data = blob.data_stream.read()
            self._size = blob.size


class Repository:
    attr_reader = property(lambda self: self.repository)

    def __init__(self, repo, commit_oid):
        self.repository = repo
        self.commit_oid = commit_oid
        self.old_commit_oid = None
        self.old_stats = None

        if not isinstance(commit_oid, str):
            raise TypeError('commit_oid must be a commit SHA1')

    @classmethod
    def incremental(cls, repo, commit_oid, old_commit_oid, old_stats):
        repo = cls(repo, commit_oid)
        repo.load_existing_stats(old_commit_oid, old_stats)
        return repo

    def load_existing_stats(self, old_commit_oid, old_stats):
        self.old_commit_oid = old_commit_oid
        self.old_stats = old_stats

    def languages(self):
        if not hasattr(self, '_sizes'):
            sizes = {}
            for _, (language, size) in self.cache().items():
                sizes[language] = sizes.get(language, 0) + size
            self._sizes = sizes
        return self._sizes

    def language(self):
        if not hasattr(self, '_language'):
            primary = max(self.languages().items(), key=lambda x: x[1], default=(None, 0))
            self._language = primary[0]
        return self._language

    def size(self):
        if not hasattr(self, '_size'):
            self._size = sum(self.languages().values())
        return self._size

    def breakdown_by_file(self):
        if not hasattr(self, '_file_breakdown'):
            breakdown = {}
            for filename, (language, _) in self.cache().items():
                utf8_filename = filename.encode("utf-8", "ignore").decode("utf-8")
                breakdown.setdefault(language, []).append(utf8_filename)
            self._file_breakdown = breakdown
        return self._file_breakdown

    def cache(self):
        if not hasattr(self, '_cache'):
            if self.old_commit_oid == self.commit_oid:
                self._cache = self.old_stats
            else:
                self._cache = self.compute_stats(self.old_commit_oid, self.old_stats)
        return self._cache

    def read_index(self):
        attr_index = self.repository.index
        attr_index.read_tree(self.current_tree())

    def current_tree(self):
        if not hasattr(self, '_tree'):
            self._tree = self.repository.commit(self.commit_oid).tree
        return self._tree

    MAX_TREE_SIZE = 100000

    def compute_stats(self, old_commit_oid, cache=None):
        if self.current_tree().count_recursive(self.MAX_TREE_SIZE) >= self.MAX_TREE_SIZE:
            return {}

        old_tree = old_commit_oid and self.repository.commit(old_commit_oid).tree
        self.read_index()
        diff = self.repository.tree(old_tree, self.current_tree())

        if cache and any(os.path.basename(delta.new_file.path) == ".gitattributes" for delta in diff):
            diff = self.repository.tree(None, self.current_tree())
            file_map = {}
        else:
            file_map = cache.copy() if cache else {}

        for delta in diff:
            old = delta.old_file.path
            new = delta.new_file.path

            if old in file_map:
                del file_map[old]
            if delta.type != "blob":
                continue

            if delta.status in ["added", "modified"]:
                mode = delta.new_file.mode
                mode_format = (int(mode, 8) & 0o170000)
                if mode_format in [0o120000, 0o40000, 0o160000]:
                    continue

                blob = LazyBlob(self.repository, delta.new_file.hexsha, new, mode)
                self.update_file_map(blob, file_map, new)
                blob.cleanup()

        return file_map

    def update_file_map(self, blob, file_map, key):
        if blob.include_in_language_stats():
            file_map[key] = [blob.language().group().name, blob.size()]
