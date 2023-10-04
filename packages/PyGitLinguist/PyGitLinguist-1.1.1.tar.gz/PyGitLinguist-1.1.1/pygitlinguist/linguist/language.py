import json
import os
from urllib.parse import quote_plus
from collections import defaultdict
import yaml

from linguist.FileBlob import FileBlob

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
LANGUAGES_YAML_PATH = os.path.join(SCRIPT_DIR, 'languages.yml')


class Language:
    languages = []
    index = {}
    name_index = {}
    alias_index = {}
    language_id_index = {}
    extension_index = defaultdict(list)
    interpreter_index = defaultdict(list)
    filename_index = defaultdict(list)
    popular = []
    unpopular = []
    colors = []

    def __init__(self, name, fs_name=None, lang_type=None, color=None, aliases=None, language_id=None,
                 tm_scope='none', ace_mode=None, codemirror_mode=None, codemirror_mime_type=None,
                 wrap=False, extensions=None, interpreters=None, filenames=None, popular=False,
                 group_name=None):
        self.name = name
        self.fs_name = fs_name
        self.type = lang_type
        self.color = color
        self.aliases = [self.default_alias()] + (aliases or [])
        self.language_id = language_id
        self.tm_scope = tm_scope
        self.ace_mode = ace_mode
        self.codemirror_mode = codemirror_mode
        self.codemirror_mime_type = codemirror_mime_type
        self.wrap = wrap
        self.extensions = extensions or []
        self.interpreters = interpreters or []
        self.filenames = filenames or []
        self.popular = popular
        self.group_name = group_name or self.name
        self._group = None
        self._add_language(self)



    @classmethod
    def _add_language(self, language):
        Language.languages.append(language)
        Language.name_index[language.name.lower()] = language
        Language.index[language.name.lower()] = language


        for alias in language.aliases:
            Language.alias_index[alias.lower()] = language
            Language.index[alias.lower()] = language

        for ext in language.extensions:
            Language.extension_index[ext.lower()].append(language)

        for interpreter in language.interpreters:
            Language.interpreter_index[interpreter].append(language)

        for filename in language.filenames:
            Language.filename_index[filename].append(language)

        Language.language_id_index[language.language_id] = language

    def escaped_name(self):
        return quote_plus(self.name).replace('+', '%20')

    def default_alias(self):
        return self.name.lower().replace(' ', '-')

    def group(self):
        if not self._group:
            self._group = Language.find_by_name(self.group_name)
        return self._group

    def __str__(self):
        return self.name

    @classmethod
    def by_type(cls, lang_type):
        return [lang for lang in cls.languages if lang.type == lang_type]

    @classmethod
    def all(cls):
        if not cls.languages:
            cls.load()
        return cls.languages

    @classmethod
    def find_by_name(cls, name):
        if not isinstance(name, str) or not name:
            return None
        return cls.name_index.get(name.lower()) or cls.name_index.get(name.split(',', 1)[0].lower())

    @classmethod
    def find_by_alias(cls, name):
        if not isinstance(name, str) or not name:
            return None
        return cls.alias_index.get(name.lower()) or cls.alias_index.get(name.split(',', 1)[0].lower())

    @classmethod
    def find_by_filename(cls, filename):
        if not cls.filename_index:
            cls.load()
        return cls.filename_index.get(filename, [])

    @classmethod
    def find_by_extension(cls, filename):
        if not cls.extension_index:
            cls.load()
        for ext in FileBlob(filename).extensions:
            if cls.extension_index.get(ext, []):

                return cls.extension_index.get(ext, [])

    @classmethod
    def find_by_interpreter(cls, interpreter):
        if not cls.interpreter_index:
            cls.load()
        return cls.interpreter_index.get(interpreter, [])

    @classmethod
    def find_by_id(cls, language_id):
        if not cls.language_id_index:
            cls.load()
        return cls.language_id_index.get(int(language_id))

    @classmethod
    def _find_extension(cls, filename):
        if not cls.extension_index:
            cls.load()
        for ext in FileBlob(filename).extensions:
            if cls.extension_index.get(ext, []):
                return ext

    @classmethod
    def populate_popular(cls):
        cls.popular = sorted((lang for lang in cls.languages if lang.popular), key=lambda l: l.name.lower())

    @classmethod
    def populate_unpopular(cls):
        cls.unpopular = sorted((lang for lang in cls.languages if not lang.popular), key=lambda l: l.name.lower())

    @classmethod
    def populate_colors(cls):
        cls.colors = sorted((lang for lang in cls.languages if lang.color), key=lambda l: l.name.lower())

    @classmethod
    def load(cls):
        if cls.interpreter_index and cls.filename_index and cls.language_id_index and cls.extension_index:
            return
        with open(LANGUAGES_YAML_PATH, 'r') as f:
            data = yaml.safe_load(f)
        for name, lang in data.items():
            lang = data[name]
            new_language = Language(
                name=name,
                fs_name=lang.get('fs_name'),
                lang_type=lang.get('type'),
                color=lang.get('color'),
                aliases=lang.get('aliases'),
                language_id=lang.get('language_id'),
                tm_scope=lang.get('tm_scope'),
                ace_mode=lang.get('ace_mode'),
                codemirror_mode=lang.get('codemirror_mode'),
                codemirror_mime_type=lang.get('codemirror_mime_type'),
                wrap=lang.get('wrap'),
                extensions=list(set(lang.get('extensions'))) if lang.get('extensions') else None,
                interpreters=lang.get('interpreters'),
                filenames=lang.get('filenames'),
                popular=lang.get('popular'),
                group_name=lang.get('group_name')
            )
            cls._add_language(new_language)
