import re
from collections import namedtuple
from ox import Token as ox_token


"""
The jarbas_dsl lexer is used to process
an entry string of code by classifying
each "word" into a language token
"""


# This regex map is necessary to capture all valid
# tokens on a given string and also could be called
# the language alphabet 
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

# The parser used by jarbas_dsl need
# a list with all names of valid tokens
valid_tokens = [x for x, y in regex_map]

template = r'(?P<{name}>{regex})'

# This is used to create a big regex with all
# regex in regex_map to avoid compile one regex
# at a time
REGEX_ALL = '|'.join(
    template.format(name=name, regex=regex)
    for (name, regex) in regex_map
)

re_all = re.compile(REGEX_ALL)

def tokenize(source):
    """
    Return each token  of a given string based on lexer rules
    """
    token_list = []
    lineno = 1
    last = 0
    for m in re_all.finditer(source):
        type_ = m.lastgroup
        if type_ == 'SPACE':
            continue
        elif type_ == 'NEWLINE':
            lineno += 1
            continue
        i, j = m.span()
        if i > last:
            # it means that there is text between last match and this one
            token_list.append(Token('TEXT', source[last:i], lineno))
        last = j
        data = m.string[i:j]
        token_list.append(Token(type_, data, lineno))

    if last != len(source):
        token_list.append(Token('TEXT', source[last:len(source)], lineno))

    return token_list

class Token(ox_token):
    """
    The Token definition used by jarbas_dsl lexer
    is the same used by the ox-parse lib
    """
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
