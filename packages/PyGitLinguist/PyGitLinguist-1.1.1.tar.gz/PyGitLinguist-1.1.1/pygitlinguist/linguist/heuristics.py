import os
import re
import yaml
from typing import List, Union, Any
from linguist.language import Language


class Heuristics:
    HEURISTICS_CONSIDER_BYTES = 50 * 1024
    heuristics = []

    @classmethod
    def call(cls, blob, candidates):
        if blob.symlink:
            return []
        cls.load()

        data = blob.data[0:cls.HEURISTICS_CONSIDER_BYTES]

        for heuristic in cls.heuristics:
            if heuristic.matches(blob.name, candidates):
                return heuristic.call(data) or []
        return []  # No heuristics matched

    @classmethod
    def all(cls):
        cls.load()
        return cls.heuristics

    @classmethod
    def load(cls):
        if cls.heuristics:
            return

        data = cls.load_config()
        named_patterns = {k: cls.to_regex(v) for k, v in data.get('named_patterns', {}).items()}

        for disambiguation in data.get('disambiguations', []):
            exts = disambiguation.get('extensions', [])
            rules = disambiguation.get('rules', [])
            for rule in rules:
                rule['pattern'] = cls.parse_rule(named_patterns, rule)
            cls.heuristics.append(Heuristics(exts, rules))

    @staticmethod
    def load_config():
        with open(os.path.join(os.path.dirname(__file__), "heuristics.yml"), 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def parse_rule(named_patterns, rule):
        if rule.get('and'):
            return And([Heuristics.parse_rule(named_patterns, block) for block in rule['and']])
        elif rule.get('pattern'):
            return Heuristics.to_regex(rule['pattern'])
        elif rule.get('negative_pattern'):
            return NegativePattern(Heuristics.to_regex(rule['negative_pattern']))
        elif rule.get('named_pattern'):
            return named_patterns.get(rule['named_pattern'])
        else:
            return AlwaysMatch()

    @staticmethod
    def to_regex(str_pattern):
        if isinstance(str_pattern, list):
            return re.compile('|'.join([re.escape(pattern) for pattern in str_pattern]))
        else:
            return re.compile(re.escape(str_pattern))

    def __init__(self, exts=None, rules=None):
        self.exts = exts
        self.rules = rules

    def matches(self, filename, candidates):
        filename = filename.lower()
        candidates = [candidate.name for candidate in candidates if candidate]
        return any(filename.endswith(ext) for ext in self.exts)

    # def call(self, data):
    #     matched = next((rule for rule in self.rules if rule['pattern'].match(data)), None)
    #     if matched:
    #         languages = matched.get('language', [])
    #         if isinstance(languages, list):
    #             return [Language[lang] for lang in languages]
    #         else:
    #             return [Language[languages]]


class And:
    def __init__(self, pats: List[Union[Any, re.Pattern]]):
        self.pats = pats

    def match(self, input_str: str) -> bool:
        return all(pat.match(input_str) for pat in self.pats)


class AlwaysMatch:
    @staticmethod
    def match(input_str: str) -> bool:
        return True


class NegativePattern:
    def __init__(self, pat: re.Pattern):
        self.pat = pat

    def match(self, input_str: str) -> bool:
        return not self.pat.match(input_str)
