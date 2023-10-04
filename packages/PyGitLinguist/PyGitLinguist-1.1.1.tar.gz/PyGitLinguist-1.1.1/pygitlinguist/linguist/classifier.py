import math
from collections import defaultdict
from linguist.tokenizer import Tokenizer
from linguist.language import Language


class Classifier:
    CLASSIFIER_CONSIDER_BYTES = 50 * 1024

    @staticmethod
    def call(blob, possible_languages):
        from linguist.samples import Samples

        if not possible_languages:
            possible_languages = Language.all()

        language_names = [lang.name for lang in possible_languages]
        cache = Samples.cache()
        data = blob.data
        return [
            Language.find_by_name(name)  # Assuming Language is a defined construct to fetch Language objects
            for name, _ in Classifier.classify(cache, data[:Classifier.CLASSIFIER_CONSIDER_BYTES], language_names)
        ]

    @staticmethod
    def train(db, language, data):
        tokens = Tokenizer().tokenize(data) if isinstance(data, str) else data
        counts = defaultdict(int)

        for token in tokens:
            counts[token] += 1

        db.setdefault('tokens_total', 0)
        db.setdefault('languages_total', 0)
        db.setdefault('tokens', {})
        db.setdefault('language_tokens', {})
        db.setdefault('languages', {})

        for token, count in counts.items():
            db['tokens'].setdefault(language, {}).setdefault(token, 0)
            db['tokens'][language][token] += count
            db['language_tokens'].setdefault(language, 0)
            db['language_tokens'][language] += count
            db['tokens_total'] += count

        db['languages'].setdefault(language, 0)
        db['languages'][language] += 1
        db['languages_total'] += 1

    @staticmethod
    def classify(db, tokens, languages=None):
        languages = languages or list(db['languages'].keys())
        classifier = Classifier(db)
        return classifier._classify(tokens, languages)

    def __init__(self, db={}, cache={}):
        self.tokens_total = db.get('tokens_total', 0)
        self.languages_total = db.get('languages_total', 0)
        self.tokens = db.get('tokens', {})
        self.language_tokens = db.get('language_tokens', {})
        self.languages = db.get('languages', {})
        self.unknown_logprob = math.log(1 / float(self.tokens_total or 1))
        self.cache = cache

    def _classify(self, tokens, languages):
        if not tokens or not languages:
            return []
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(tokens) if isinstance(tokens, str) else tokens
        scores = {}
        counts = defaultdict(int)

        for token in tokens:
            counts[token] += 1

        for language in languages:
            scores[language] = self.tokens_probability(counts, language) + self.language_probability(language)

        return sorted(((language, score) for language, score in scores.items()), key=lambda x: x[1], reverse=True)

    def tokens_probability(self, counts, language):
        return sum(count * self.token_probability(token, language) for token, count in counts.items())

    def token_probability(self, token, language):
        count = self.tokens.get(language, {}).get(token, 0)
        if count == 0:
            return self.unknown_logprob
        return math.log(count / float(self.language_tokens.get(language, 1)))

    def language_probability(self, language):
        return math.log(self.languages.get(language, 1) / float(self.languages_total or 1))
