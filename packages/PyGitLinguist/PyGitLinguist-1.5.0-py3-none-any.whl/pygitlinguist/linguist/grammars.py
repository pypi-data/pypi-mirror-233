import os

class Grammars:
    @staticmethod
    def path():
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../grammars"))
