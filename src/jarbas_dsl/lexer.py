import re
from collections import namedtuple
from ox import Token as ox_token
import ox


"""
The jarbas_dsl lexer is used to process
an entry string of code by classifying
each "word" into a language token
"""


# This regex map is necessary to capture all valid
# tokens on a given string and also could be called
# the language alphabet
regex_pairs = [
    ('NUMBER', r'([0-9]+\.[0-9]+)|([0-9]+)'),
    ('STRING', r'\'.*\''),
    ('BOOLEAN', r'True|False'),
    ('OUTPUT_VAR', r'\$[a-zA-Z][a-zA-Z0-9_]*'),
    ('OUTPUT_ATTR', r'\.[a-zA-Z][a-zA-Z0-9_]*'),
    ('NAME', r'[a-zA-Z][a-zA-Z0-9_]*'),
    ('ATTRIB', r'\.[a-zA-Z]([a-zA-Z0-9_]*)'),
    ('PIPE_FILTER', r'\|[a-zA-Z]([a-zA-Z0-9_]*)'),
    ('COMMENT', r'//.*'),
    ('PAREN_O', r'\('),
    ('PAREN_C', r'\)'),
    ('BRACKET_O', r'\['),
    ('BRACKET_C', r'\]'),
    ('CONDITIONAL_IF', r'=if +'),
    ('CONDITIONAL_ELIF', r'=elif +'),
    ('CONDITIONAL_ELSE', r'=else\n+'),
    ('END_CONDITIONAL', r'=endif+'),
    ('AMPER', r'=&'),
    ('AT', r'=@'),
    ('EQUAL', r'='),
    ('NEWLINE', r'\n'),
    ('SPACE', r'\s+'),
]

regex_map = {k: (k, v) for k, v in regex_pairs}

# The parser used by jarbas_dsl need
# a list with all names of valid tokens
valid_tokens = [x for x in regex_map]
valid_tokens.append('TEXT')

template = r'(?P<{name}>{regex})'


input_pattern = re.compile(r'\[.*\]$')
control_pattern = re.compile(r'\=if')
output_pattern = re.compile(r'\$.+')

class Lexer():

    def __init__(self, src):
        self.src = src
        self.line_stack = list(reversed(self.src.split('\n')))


    def tokenize(self):
        while self.line_stack:
            line = normalize_line(self.line_stack.pop())
            print()
            if input_pattern.match(line):
                yield from self.tokenize_input_line(line)
            elif control_pattern.match(line):
                ...
            else:
              yield from self.tokenize_output_line(line)


    def tokenize_input_line(self, line):
        start, _, end = line.rpartition('[')
        input_data = end[:-1]
        yield from self.tokenize_output_line(line)
        yield Token('START_INPUT', '[')
        yield from input_lexer(input_data)
        yield Token('END_INPUT', ']')

    def tokenize_output_line(self, line):
        yield from output_lexer(line)


input_lexer = ox.make_lexer([
    regex_map['NAME'],
    regex_map['EQUAL'],
    regex_map['AMPER'],
    regex_map['AT'],
])

output_lexer = ox.make_lexer([
    regex_map['OUTPUT_VAR'],
    regex_map['OUTPUT_ATTR'],
])


def tokenize(source):
    lex = Lexer(source)
    return list(lex.tokenize())

def normalize_line(line):
    return line.partition('//')[0].rstrip()

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


s = '$person // simple input'
a = tokenize(s)
print(a)