import os

class FileBlob:
    def __init__(self, file_name):
        self.file_name = file_name.lower()  # Assuming a case insensitive comparison
        self.base_name = os.path.basename(self.file_name)
        self.extensions = self.get_extensions()

    def get_extensions(self):
        name, extension = os.path.splitext(self.base_name)
        extensions = []
        while extension:
            extensions.append(extension)
            name, extension = os.path.splitext(name)
        return extensions[::-1]  # Reversing, as splitext gets the last extension first
