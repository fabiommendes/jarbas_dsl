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
                          ('COMMENT', r'//.*'),
                          ('PARENTHESES_O', r'\('),
                          ('PARENTHESES_C', r'\)'),
                          ('BRACKET_O', r'\['),
                          ('BRACKET_C', r']'),
                          ('EQUAL', r'='),
                          ('AMPER', r'&'),
                          ('AT', r'@'),
                          ('NEWLINE', r'\n'),
                          ('SPACE', r'\s+'),
                          ('CONDITIONAL_IF', r'[if]+\s\$[a-zA-Z]+')]

        # Template used to map a regex to a name
        self.template = r'(?P<{name}>{regex})'

        # Creating a big regex for jarbas dsl
        self.REGEX_ALL = '|'.join(
            self.template.format(name=name, regex=regex)
            for (name, regex) in self.regex_map
        )

        self.re_all = re.compile(self.REGEX_ALL)
        self.token_list = []


    def tokenize(self, source):
        """
        Create a list of tokens based on lexer rules and text passed as string
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
    lexer = Lexer()
    l = list(lexer.tokenize(source))
    return l
