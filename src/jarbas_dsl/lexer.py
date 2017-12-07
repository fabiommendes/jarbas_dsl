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
    ('OUTPUT_VAR', r'\$[a-zA-Z_]\w*'),
    ('OUTPUT_ATTR', r'\.[a-zA-Z_]\w*'),
    ('NAME', r'[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)*'),
    ('PIPE_FILTER', r'\|'),
    ('START_INPUT', r'\['),
    ('END_INPUT', r'\]'),
    ('SIMPLE_IF', r'=if +'),
    ('OUTPUT_IF', r'=if= +'),
    ('SIMPLE_ELIF', r'=elif +'),
    ('OUTPUT_ELIF', r'=elif= +'),
    ('SIMPLE_ELSE', r'=else+'),
    ('END_CONTROL', r'=endif+'),
    ('AMPER', r'=&'),
    ('AT', r'=@'),
    ('EQUAL', r'='),
]

regex_map = {k: (k, v) for k, v in regex_pairs}

# The parser used by jarbas_dsl need
# a list with all names of valid tokens
valid_tokens = [x for x in regex_map]
valid_tokens.append('TEXT')


input_pattern = re.compile(r'.*\[.*\]$')
control_pattern = re.compile(r'\=if\=|\=elif\=|\=if|\=elif|\=else|\=endif')
output_pattern = re.compile(r'\$[a-zA-Z_]\w*(\.[a-zA-Z_]\w*)*')
output_line_pattern = re.compile(r'.*\$[a-zA-Z_]\w*')
filter_pattern = re.compile(r'\|[a-zA-Z_]\w*')


input_lexer = ox.make_lexer([
    regex_map['NAME'],
    regex_map['EQUAL'],
    regex_map['AMPER'],
    regex_map['AT'],
    regex_map['START_INPUT'],
    regex_map['END_INPUT'],
])

output_lexer = ox.make_lexer([
    regex_map['OUTPUT_VAR'],
    regex_map['OUTPUT_ATTR'],
    regex_map['NAME'],
    regex_map['PIPE_FILTER'],
])

control_lexer = ox.make_lexer([
    regex_map['SIMPLE_IF'],
    regex_map['OUTPUT_IF'],
    regex_map['SIMPLE_ELIF'],
    regex_map['OUTPUT_ELIF'],
    regex_map['SIMPLE_ELSE'],
    regex_map['END_CONTROL'],
])


class Lexer():

    def __init__(self, src):
        self.src = src
        self.line_stack = list(reversed(self.src.split('\n')))


    def tokenize(self):
        while self.line_stack:
            line = normalize_line(self.line_stack.pop())

            if control_pattern.match(line):
                yield from self.tokenize_control_line(line)
            elif input_pattern.match(line):
                yield from self.tokenize_input_line(line)
            elif output_line_pattern.match(line):
                yield from self.tokenize_output_line(line)
            else:
                yield Token('TEXT', line)


    def tokenize_input_line(self, line):
        _, start, end = line.rpartition('[')

        if start != '':
            input_data = end[:-1]
            yield from self.tokenize_output_line(_)
            yield from input_lexer('[%s]' % input_data)
        else:
            yield from self.tokenize_output_line(end)


    def tokenize_output_line(self, line):
        while line:
            match = output_pattern.search(line)

            if match is None:
                yield Token('TEXT', line)
                break
            else:
                i, j = match.span()
                if i != 0:
                    yield Token('TEXT', line[0:i])

                yield from output_lexer(line[i:j])
                
                line = line[j:]
                match = filter_pattern.search(line)

                if line == '':
                    break
                elif match is None:
                    yield Token('TEXT', line)
                    break
                else:
                    i, j = match.span()
                    if i != 0:
                        yield Token('TEXT', line[0:i])

                    yield from output_lexer(line[i:j])
                    line = line[j:]


    def tokenize_control_line(self, line):
        match = control_pattern.match(line)
        i, j = match.span()
        yield from control_lexer(line[i:j])
        yield from self.tokenize_input_line(line[j + 1:]) 


def normalize_line(line):
    return line.partition('//')[0].rstrip()


def tokenize(source):
    lex = Lexer(source)
    return list(lex.tokenize())


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
