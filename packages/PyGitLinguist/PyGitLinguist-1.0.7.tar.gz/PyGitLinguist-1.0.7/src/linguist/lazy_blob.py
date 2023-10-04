from lang_detect import blob_helper
from linguist.language import Language
from git import GitConfigParser
from git import Repo


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
            config_parser = GitConfigParser()
            config_parser.read(self.repository.git_dir + "/config")
            self._git_attributes = config_parser.items("attr " + self.name)

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
            repo = Repo(self.repository.working_dir)
            commit = repo.commit(self.oid)
            blob = commit.tree / self.name
            self._data = blob.data_stream.read()
            self._size = blob.size
