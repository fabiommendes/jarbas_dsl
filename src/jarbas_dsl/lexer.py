import re
from collections import namedtuple

# Token definition of this lexer
class Token(namedtuple('Token', ['type', 'data', 'lineno'])):
    """
    gyug ygytg ytg ytgy
    """

    def __eq__(self, other):
        if isinstance(other, str):
            return self.data == other
        else:
            return super().__eq__(other)

class Lexer:
    """
    gyug ygytg ytg ytgy
    """

    def __init__(self):

        # Regex map to capture language tokens
        self.regex_map = [('NUMBER', r'[0-9]+'),
                          ('VARIABLE', r'\$[a-zA-Z]([a-zA-Z0-9_]*)'),
                          ('ATTRIB', r'\.[a-zA-Z]([a-zA-Z0-9_]*)'),
                          ('PIPE', r'\|'),
                          ('COMMENT_MARKER', r'//'),
                          ('PARENTHESES_O', r'\('),
                          ('PARENTHESES_C', r'\)'),
                          ('NEWLINE', r'\n'),
                          ('SPACE', r'\s+'),
                          ('TEXT', r'\s*.+\s+')]

        # Template used to map a regex to a name
        self.template = r'(?P<{name}>{regex})'

        # Creating a big regex for jarbas dsl
        self.REGEX_ALL = '|'.join(
            self.template.format(name=name, regex=regex)
            for (name, regex) in self.regex_map
        )

        self.re_all = re.compile(self.REGEX_ALL)
        self.token_list = []

    # Create a list of tokens based on lexer rules and text passed as string
    def tokenize(self, source):

        lineno = 1
        for m in self.re_all.finditer(source):
            type_ = m.lastgroup
            if type_ == 'SPACE':
                continue
            elif type_ == 'NEWLINE':
                lineno += 1
                continue
            i, j = m.span()
            data = m.string[i:j]
            self.token_list.append(Token(type_, data, lineno))

        return self.token_list


def tokenize(source):
    lexer = Lexer()
    return lexer.tokenize(source)
