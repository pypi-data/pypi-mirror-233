import json
import mimetypes
import cgi
import chardet
import re
import yaml
from typing import Optional, List, Union
from lang_detect import Linguist
from linguist.language import Language

MEGABYTE = 1024 * 1024


class BlobHelper:
    def __init__(self, name: str, data: Optional[str], size: int):
        self.name = name
        self.data = data
        self.size = size
        self._mime_type = None
        self._detect_encoding = None
        self.content_type = None
        self._encoded_newlines_re = None
        self._lines = None
        self._language = None

    def extname(self) -> str:
        return mimetypes.guess_extension(self.name) or ""

    def get_mime_type(self) -> Optional[mimetypes.MimeTypes]:
        if self._mime_type:
            return self._mime_type
        self._mime_type = mimetypes.guess_type(self.name)[0]
        return self._mime_type

    def mime_type(self) -> str:
        return self._mime_type() or 'text/plain'

    def binary_mime_type(self) -> bool:
        return self.get_mime_type() and self._mime_type.startswith('application/')

    def likely_binary(self) -> bool:
        # The Language.find_by_filename equivalent is not available in Python, so you might need to implement that
        # based on your specific use case.
        return self.binary_mime_type() and not Language.find_by_filename(self.name)

    def content_type(self) -> str:
        if self.content_type:
            return self.content_type
        self.content_type = self.mime_type() if self.binary_mime_type() or self.binary() else \
            f"text/plain; charset={self.encoding.lower()}" if self.encoding else "text/plain"
        return self.content_type

    def disposition(self) -> str:
        if self.text() or self.image():
            return 'inline'
        return "attachment" if not self.name else f"attachment; filename={cgi.escape(self.name)}"

    def detect_encoding(self) -> Optional[dict]:
        if self._detect_encoding or not self.data:
            return self._detect_encoding
        self._detect_encoding = chardet.detect(self.data.encode())
        return self._detect_encoding

    def encoding(self) -> Optional[str]:
        if detect_enc := self.detect_encoding():
            return detect_enc['encoding']
        return None

    def ruby_encoding(self) -> Optional[str]:
        if detect_enc := self.detect_encoding():
            print(detect_enc)
            return detect_enc.get('ruby_encoding')
        return None

    def binary(self) -> bool:
        if self.data is None:
            return True
        if self.data == "":
            return False
        if not self.encoding:
            return True
        return self.detect_encoding().get('type') == 'binary'

    def empty(self) -> bool:
        return self.data is None or self.data == ""

    def text(self) -> bool:
        return not self.binary()

    def image(self) -> bool:
        return self.extname().lower() in ['.png', '.jpg', '.jpeg', '.gif']

    def solid(self) -> bool:
        return self.extname().lower() == '.stl'

    def csv(self) -> bool:
        return self.text() and self.extname().lower() == '.csv'

    def pdf(self) -> bool:
        return self.extname().lower() == '.pdf'

    def large(self) -> bool:
        return int(self.size) > MEGABYTE

    def safe_to_colorize(self) -> bool:
        return not self.large() and self.text() and not self.high_ratio_of_long_lines()

    def high_ratio_of_long_lines(self) -> bool:
        return False if self.loc() == 0 else self.size / self.loc() > 5000

    def viewable(self) -> bool:
        return not self.large() and self.text()

    def vendored(self) -> bool:
        with open("../vendor.yml", 'r') as file:
            vendored_paths = yaml.safe_load(file)
        vendored_regexp = re.compile('|'.join(vendored_paths))
        return bool(vendored_regexp.match(self.name))

    def documentation(self) -> bool:
        with open("../documentation.yml", 'r') as file:
            documentation_paths = yaml.safe_load(file)
        documentation_regexp = re.compile('|'.join(documentation_paths))
        return bool(documentation_regexp.match(self.name))

    def lines(self) -> List[str]:
        if self._lines or not (self.viewable() and self.data):
            return self._lines or []
        # Similar to Ruby equivalent, split by detected encoding
        # Re-encode each newline sequence as detected encoding
        try:
            self._lines = re.split(self.encoded_newlines_re(), self.data.rstrip('\r\n'))
        except LookupError:  # Equivalent to Encoding::ConverterNotFoundError
            self._lines = [self.data]
        return self._lines

    def encoded_newlines_re(self) -> re.Pattern:
        if self._encoded_newlines_re:
            return self._encoded_newlines_re
        newlines = ["\r\n", "\r", "\n"]
        encoded_newlines = [nl.encode(self.encoding(), "ASCII-8BIT").decode(self.encoding()) for nl in newlines]
        self._encoded_newlines_re = re.compile("|".join(encoded_newlines))
        return self._encoded_newlines_re

    def first_lines(self, n: int) -> List[str]:
        if self._lines:
            return self._lines[0:n]
        if not (self.viewable() and self.data):
            return []
        i, c = 0, 0
        while c < n and (match := re.search(self.encoded_newlines_re(), self.data[i:])) is not None:
            j = match.start() + i  # Adjusting start index of the found match
            i = j + len(match.group())  # Adjusting end index of the found match
            c += 1
        return re.split(self.encoded_newlines_re(), self.data[0:i], maxsplit=-1)

    def last_lines(self, n: int) -> List[str]:
        if self._lines:
            return self._lines[-n:] if n < len(self._lines) else self._lines
        if not (self.viewable() and self.data):
            return []
        no_eol = True
        i, c, k = len(self.data), 0, len(self.data)
        matches = [m for m in re.finditer(self.encoded_newlines_re(), self.data[:i])]
        while c < n and matches:
            match = matches.pop()  # Get the rightmost match
            j = match.start()
            if c == 0 and j + len(match.group()) == k:
                no_eol = False
            i = j
            c += 1

        l = i + len(self.data[i:k]) if no_eol else i
        return re.split(self.encoded_newlines_re(), self.data[l:k])

    def loc(self) -> int:
        return len(self.lines())

    def sloc(self) -> int:
        return len([line for line in self.lines() if line.strip() != ''])

    def words(self) -> int:
        return sum(len(line.split()) for line in self.lines())
