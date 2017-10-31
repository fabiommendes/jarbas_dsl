import re
from collections import namedtuple
from ox import Token


class _Token(namedtuple('Token', ['type', 'data', 'lineno'])):
    """
    Token definition used by jarbas_dsl lexer
    """

    lexpos = None
    lexer = None

    @property
    def value(self):
        return self.data

    def __new__(self, type, data, lineno):
        print(type, data, lineno)
        hash((type, data, lineno))
        return super().__new__(self, type, data, lineno)

    def __hash__(self):
        return hash((self.type, self.data, self.lineno))

    def __eq__(self, other):
        if isinstance(other, str):
            return self.data == other
        else:
            return super().__eq__(other)

class Token(Token):
    def __gt__(self, other):
        if isinstance(other, Token):
            return self.value > other.value
        elif isinstance(other, str):
            return self.value > other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Token):
            return self.value < other.value
        elif isinstance(other, str):
            return self.value < other
        return NotImplemented

regex_map = [('NUMBER', r'[0-9]+'),
                    ('VARIABLE', r'\$[a-zA-Z]([a-zA-Z0-9_]*)'),
                    ('ATTRIB', r'\.[a-zA-Z]([a-zA-Z0-9_]*)'),
                    ('PIPE_FILTER', r'\|[a-zA-Z]([a-zA-Z0-9_]*)'),
                    ('COMMENT', r'//.*'),
                    ('PARENTHESES_O', r'\('),
                    ('PARENTHESES_C', r'\)'),
                    ('BRACKET_O', r'\['),
                    ('BRACKET_C', r'\]'),
                    ('CONDITIONAL_IF', r'=if +'),
                    ('CONDITIONAL_ELIF', r'=elif +'),
                    ('CONDITIONAL_ELSE', r'=else\n+'),
                    ('END_CONDITIONAL', r'=endif+'),
                    ('EQUAL', r'='),
                    ('AMPER', r'&'),
                    ('AT', r'@'),
                    ('NEWLINE', r'\n'),
                    ('SPACE', r'\s+')]

token_list = [x for x, y in regex_map]

class Lexer:
    """
    This class process jarbas_dsl tokens from a given string of code
    """
    def __init__(self):
        # Regex map to capture language tokens

        # Template used to map a regex to a name
        self.template = r'(?P<{name}>{regex})'

        # Creating a big regex for all jarbas_dsl tokens
        self.REGEX_ALL = '|'.join(
            self.template.format(name=name, regex=regex)
            for (name, regex) in regex_map
        )

        self.re_all = re.compile(self.REGEX_ALL)


    def tokenize(self, source):
        """
        Return each token  of a given string based on lexer rules
        """
        lineno = 1
        last = 0
        for m in self.re_all.finditer(source):
            type_ = m.lastgroup
            if type_ == 'SPACE':
                continue
            elif type_ == 'NEWLINE':
                lineno += 1
                continue
            i, j = m.span()
            if i > last:
                # it means that there is text between last match and this one
                yield Token('TEXT', source[last:i], lineno)
            last = j
            data = m.string[i:j]
            yield Token(type_, data, lineno)

        if last != len(source):
            yield Token('TEXT', source[last:len(source)], lineno)


def tokenize(source):
    """
    Facilitates the use of the tokenize method by allowing the user
    to not instantiate a lexer object only to call the method
    """
    lexer = Lexer()
    token_list = list(lexer.tokenize(source))
    return token_list
