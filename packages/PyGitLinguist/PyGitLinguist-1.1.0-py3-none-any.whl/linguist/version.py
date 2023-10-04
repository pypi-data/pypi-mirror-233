import os


class Version:
    VERSION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../VERSION'))

    @classmethod
    def get_version(cls):
        with open(cls.VERSION_FILE_PATH, 'r') as version_file:
            return version_file.read().strip()