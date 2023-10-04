import re
from linguist.language import Language


class XML:
    SEARCH_SCOPE = 2

    @staticmethod
    def call(blob, candidates=[]):
        if candidates:
            return candidates

        header = "\n".join(blob.first_lines(XML.SEARCH_SCOPE))

        if re.search(r'<?xml version=', header):
            return [Language["XML"]]

        return []
