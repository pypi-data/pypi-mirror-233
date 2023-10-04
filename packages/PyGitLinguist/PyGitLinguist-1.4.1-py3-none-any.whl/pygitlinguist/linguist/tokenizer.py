import re
import tokenize
import io
from enum import Enum


class TokenType(Enum):
    KEYWORD = 'Keyword'
    IDENTIFIER = 'Identifier'
    OPERATOR = 'Operator'
    LITERAL = 'Literal'
    COMMENT = 'Comment'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Token:
    def __init__(self, token_type, value, start_line, start_col):
        self.type = token_type.value  # Access the enum value
        self.value = value
        self.start_line = start_line
        self.start_col = start_col

    def __str__(self):
        return f'{self.type} - {self.value} - {self.start_line} - {self.start_col}'

    def __repr__(self):
        return f'{self.type} - {self.value} - {self.start_line} - {self.start_col}'

    def __eq__(self, other):
        return (
                isinstance(other, Token) and
                self.type == other.type and
                self.value == other.value and
                self.start_line == other.start_line and
                self.start_col == other.start_col
        )

    def __hash__(self):
        return hash((self.type, self.value, self.start_line, self.start_col))

    def key(self):
        return f"{self.type}-{self.value}-{self.start_line}-{self.start_col}"

    def __instancecheck__(self, instance):
        return isinstance(instance, Token) or isinstance(instance, TokenType)


class Tokenizer:
    def __init__(self):
        self.tokens = []

    def tokenize(self, data):
        self.tokens = []

        # Create a StringIO object to simulate a file-like object
        data_io = io.StringIO(data)

        # Use Python's tokenize module to tokenize the code
        # catch eof errors from generate_tokens
        try:
            for tok in tokenize.generate_tokens(data_io.readline):
                token_type, token_value, (start_line, start_col), _, _ = tok
                token = Token(self.map_token_type(token_type), token_value, start_line, start_col)
                self.tokens.append(token)
        except tokenize.TokenError as e:
            # print(f'TokenError: {e} - {data_io.readline()}')
            pass
        except IndentationError as e:
            # print(f'IndentationError: {e} - {data_io.readline()}')
            pass
        return self.tokens

    @staticmethod
    def map_token_type(token_type):
        if token_type == tokenize.NAME or token_type == tokenize.NAME:
            return TokenType.IDENTIFIER
        elif token_type == tokenize.OP:
            return TokenType.OPERATOR
        elif token_type == tokenize.NUMBER or token_type == tokenize.STRING:
            return TokenType.LITERAL
        elif token_type == tokenize.COMMENT:
            return TokenType.COMMENT
        else:
            return TokenType.KEYWORD

    def remove_comments_and_strings(self, data):
        # Remove comments and string literals from the code
        # This is useful when you want to analyze the remaining code structure
        pattern = r'(#.*?$|\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\")'
        return re.sub(pattern, '', data, flags=re.MULTILINE | re.DOTALL)

    def __str__(self):
        return '\n'.join([str(token) for token in self.tokens])

    def __repr__(self):
        return '\n'.join([str(token) for token in self.tokens])

    def __hash__(self):
        # Define a custom hash method based on the properties you want to use as keys
        # For example, you can use a hash of the tuple of these properties
        return hash(tuple(self.tokens))

    def __eq__(self, other):
        # Define equality comparison to avoid hash collisions
        if isinstance(other, Tokenizer):
            return self.tokens == other.tokens
        return False

    def __instancecheck__(self, instance):
        return isinstance(instance, Tokenizer) or isinstance(instance, Token)
