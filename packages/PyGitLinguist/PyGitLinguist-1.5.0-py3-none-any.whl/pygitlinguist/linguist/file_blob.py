import os


class FileBlob:
    def __init__(self, path, base_path=None):
        self.fullpath = path
        self.path = os.path.relpath(path, start=base_path) if base_path else path
        self._mode = None
        self._symlink = None
        self._data = None
        self._size = None

    @property
    def mode(self):
        if self._mode is None:
            self._mode = oct(os.stat(self.fullpath).st_mode)[-6:]
        return self._mode

    @property
    def symlink(self):
        if self._symlink is None:
            try:
                self._symlink = os.path.islink(self.fullpath)
            except Exception:
                self._symlink = False
        return self._symlink

    @property
    def data(self):
        if self._data is None:
            with open(self.fullpath, 'rb') as f:
                self._data = f.read()
        return self._data

    @property
    def size(self):
        if self._size is None:
            self._size = os.path.getsize(self.fullpath)
        return self._size
