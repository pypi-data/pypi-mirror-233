import os
import yaml
from linguist.language import Language


class Extension:
    # Public: Use the file extension to detect the blob's language.
    #
    # blob               - An object that quacks like a blob.
    # candidates         - A list of candidate languages.
    #
    # Examples
    #
    #   Extension.call(FileBlob.new("path/to/file"))
    #
    # Returns a list of languages associated with a blob's file extension.
    # Selected languages must be in the candidate list, except if it's empty,
    # in which case any language is a valid candidate.
    @staticmethod
    def call(blob, candidates):
        if Extension.generic(blob.name):
            return candidates
        languages = Language.find_by_extension(blob.name)
        return list(set(candidates).union(set(languages)))

    # Public: Return True if the filename uses a generic extension.
    @staticmethod
    def generic(filename):
        Extension.load()
        return any(filename.lower().endswith(ext) for ext in Extension.generic_extensions)

    generic_extensions = []

    # Internal: Load the contents of `generic.yml`
    @classmethod
    def load(cls):
        if cls.generic_extensions:
            return

        current_dir = os.path.dirname(os.path.abspath(__file__))
        yml_path = os.path.join(current_dir, "..","generic.yml")

        with open(yml_path, 'r', encoding='utf-8') as yml_file:
            data = yaml.safe_load(yml_file)
            cls.generic_extensions = data['extensions']
