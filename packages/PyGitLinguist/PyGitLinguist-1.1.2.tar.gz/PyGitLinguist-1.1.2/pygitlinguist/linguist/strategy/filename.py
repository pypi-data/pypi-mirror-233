from linguist.language import Language

class Filename:
    # Public: Use the filename to detect the blob's language.
    #
    # blob               - An object that quacks like a blob.
    # candidates         - A list of candidate languages.
    #
    # Examples
    #
    #   Filename.call(FileBlob.new("path/to/file"))
    #
    # Returns a list of languages associated with a blob's filename.
    # Selected languages must be in the candidate list, except if it's empty,
    # in which case any language is a valid candidate.
    @staticmethod
    def call(blob, candidates):
        name = blob.name
        languages = Language.find_by_filename(name)
        return candidates if not candidates else list(set(candidates) & set(languages))
