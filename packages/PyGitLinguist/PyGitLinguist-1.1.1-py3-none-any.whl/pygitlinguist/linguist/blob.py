import os
from linguist.blob_helper import BlobHelper  # adjust the import according to your project structure


class Blob:
    def __init__(self, path, content='', symlink=False):
        self.path = path
        self.content = content
        if not content:
            self.from_path()
        self.symlink = symlink
        self.blob_helper = BlobHelper(name=os.path.basename(self.path), data=self.content, size=self.size)

    def from_path(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            self.content = file.read()

    @property
    def name(self):
        return self.blob_helper.name

    @property
    def data(self):
        return self.blob_helper.data

    @property
    def size(self):
        return len(self.content.encode('utf-8'))

    @property
    def extension(self):
        return self.extensions[-1] if self.extensions else ""

    @property
    def extensions(self):
        segments = self.name.lower().split(".")[1:]
        return ["." + ".".join(segments[i:]) for i in range(len(segments))]

    def is_symlink(self):
        return self.symlink

    def get_mime_type(self):
        return self.blob_helper.mime_type

    def is_text(self):
        return self.blob_helper.text()

    def is_image(self):
        return self.blob_helper.image()

    def likely_binary(self):
        return self.blob_helper.likely_binary()

    def detect_encoding(self):
        return self.blob_helper.detect_encoding()

    def ruby_encoding(self):
        return self.blob_helper.ruby_encoding()

    def binary(self):
        return self.blob_helper.binary()

    @property
    def binary_mime_type(self):
        return self.blob_helper.binary_mime_type()

    @property
    def content_type(self):
        return self.blob_helper.content_type()

    @property
    def disposition(self):
        return self.blob_helper.disposition()

    @property
    def encoding(self):
        return self.blob_helper.encoding()

    @property
    def is_generated(self):
        return self.blob_helper.generated()

    @property
    def is_vendored(self):
        return self.blob_helper.vendored()

    @property
    def loc(self):
        return self.blob_helper.loc()

    @property
    def sloc(self):
        return self.blob_helper.sloc()

    def empty(self):
        return self.blob_helper.empty()

    def first_lines(self, n=10):
        return self.blob_helper.first_lines(n)

    def last_lines(self, n=10):
        return self.blob_helper.last_lines(n)
