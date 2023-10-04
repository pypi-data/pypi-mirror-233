from linguist.heuristics import Heuristics
from linguist.shebang import Shebang
from linguist.strategy.manpage import Manpage
from linguist.strategy.xml import XML
from linguist.strategy.modeline import Modeline as LinguistStrategyModeline
from linguist.strategy.filename import Filename as LinguistStrategyFilename
from linguist.strategy.extension import Extension as LinguistStrategyExtension
from linguist.classifier import Classifier


class Linguist:

    @staticmethod
    def detect(blob, allow_empty=False):
        if blob.likely_binary() or blob.binary() or (not allow_empty and blob.empty()):
            return None
        languages = []
        returning_strategy = None

        strategies = [
            LinguistStrategyModeline(),
            LinguistStrategyFilename(),
            Shebang(),
            LinguistStrategyExtension(),
            XML(),
            Manpage(),
            Heuristics(),
            # Classifier()
        ]

        for strategy in strategies:
            returning_strategy = strategy

            candidates = strategy.call(blob, languages)
            candidates = list(filter(lambda x: x is not None, candidates))
            if len(candidates) == 1:
                languages.extend(candidates)
                break
            elif len(candidates) > 1:
                languages.extend(candidates)
            else:
                pass
        return languages[0] if languages else None

    instrumenter = None

    @classmethod
    def instrument(cls, *args, **kwargs):
        if cls.instrumenter:
            cls.instrumenter.instrument(*args, **kwargs)
        elif 'block' in kwargs:
            kwargs['block']()
