import re
from linguist.language import Language


class Modeline:
    EMACS_MODELINE = re.compile(r"-\*-(?:(?:[ \t]*(?=[^:;\s]+[ \t]*-\*-))|(?:(?:.*?[ \t;])|(?<=-\*-)))[ \t]*mode[ \t]*:[ \t]*([^:;\s]+)(?=[ \t;]|(?<![-*])-\*-).*?-*-", re.IGNORECASE)

    VIM_MODELINE = re.compile(r"((?:(?:^|[ \t])(?:vi|Vi(?=m))(?:(?:m[<=>]?[0-9]+)|m)?)|[ \t]ex)(?=: (?=[ \t]* set? [ \t] [^\r\n:]+ :)|: (?![ \t]* set? [ \t]))(?:(?:(?:[ \t]* : [ \t]*)|[ \t])\w*(?:[ \t]*=(?:[^\\\s]|\\.)*[^\\\s]?)?)*(?:[ \t:] (?:filetype|ft|syntax)[ \t]*=(\w+)(?=$|\s|:))", re.IGNORECASE)

    MODELINES = [EMACS_MODELINE, VIM_MODELINE]

    SEARCH_SCOPE = 5

    @staticmethod
    def call(blob, _=None):
        if blob.symlink:
            return []
        header = "\n".join(blob.first_lines(Modeline.SEARCH_SCOPE))
        footer = "\n".join(blob.last_lines(Modeline.SEARCH_SCOPE))

        if "UseVimball" in header:
            return []
        return [Language.find_by_alias(Modeline.modeline(header + footer))]

    @staticmethod
    def modeline(data):
        for regex in Modeline.MODELINES:
            match = regex.search(data)
            if match:
                return match.group(1)
        return None
