import sys
import ox
from lexer import tokenize, valid_tokens
from collections import namedtuple


Var = namedtuple('Var', 'id')
Attr = namedtuple('Attr', 'id')
Method = namedtuple('Method', 'id args')
Filter = namedtuple('Filter', 'id')
Expr = namedtuple('Expr', 'components')
Text = namedtuple('Text', 'value')
Num = namedtuple('Num', 'value')
Bool = namedtuple('Bool', 'value')
Str = namedtuple('Str', 'value')
Comment = namedtuple('Comment', 'value')
Input = namedtuple('Input', 'save_in type default validate_func')

# Arguments of a method must be separated
# by a single comma in the format "method(arg1,arg2)"
# or "method(arg1, arg2)", any other format will result
# in a method with args = None
def multi_arg(arg1, text, arg2):
    if text == ', ' or text == ',':
        args = [arg1, arg2]
        return args

def normal_input(b_o, s, b_c):
    return Input(save_in=s, type=None, default=None, validate_func=None)

def type_input(b_o, s, eq, t, b_c):
    return Input(save_in=s, type=t, default=None, validate_func=None)

def default_input(b_o, s, eq, at, d, b_c):
    return Input(save_in=s, type=None, default=d, validate_func=None)

def func_input(b_o, s, eq, ap, f, b_c):
    return Input(save_in=s, type=None, default=None, validate_func=f)


parser_rules = [
    ('expr : expr expr', lambda x,y : Expr(components=[x, y])),
    ('expr : access', lambda x: x),
    ('access : ATTRIB PAREN_O PAREN_C', lambda m, p_o, p_c : Method(m.replace('.', ''), None)),
    ('access : ATTRIB PAREN_O args PAREN_C', lambda m, p_o, a, p_c : Method(m.replace('.', ''), a)),
    ('access : ATTRIB', lambda token : Attr(id=token.replace('.', ''))),
    ('access : VARIABLE', lambda token : Var(id=token.replace('$', ''))),
    ('access : PIPE_FILTER', lambda token : Filter(id=token.replace('|', ''))),
    ('access : BRACKET_O TEXT BRACKET_C', normal_input),
    ('access : BRACKET_O TEXT EQUAL TEXT BRACKET_C', type_input),
    ('access : BRACKET_O TEXT EQUAL AT TEXT BRACKET_C', default_input),
    ('access : BRACKET_O TEXT EQUAL AMPER TEXT BRACKET_C', func_input),
    ('args : arg TEXT args', multi_arg),
    ('args : arg', lambda token : token),
    ('expr : text', lambda x: x),
    ('expr : comment', lambda x: x),
    ('arg : NUMBER', lambda token : Num(value=token)),
    ('arg : BOOLEAN', lambda token : Bool(value=token)),
    ('arg : STRING', lambda token : Str(value=token.replace("'", ''))),
    ('text : TEXT', lambda token : Text(value=token)),
    ('comment : COMMENT', lambda token: Comment(value=token)),
]

parser = ox.make_parser(parser_rules, valid_tokens)

class Parser:
    """
    Parse a string of Jarbas DSL code. 
    It creates an AST object which is returned by the Parser.parse() method.
    """

    def __init__(self, source):
        self.source = source
        self.tokens = tokenize(source)
        #print(self.tokens)

    def parse(self):
        """
        Parse input source code and return a Jarbas DSL AST.
        """
        return parser(self.tokens)

#s = "Hello $person|title! //alou"
s = "Name: [name] // string input"
p = Parser(s)
#a = p.test()
#print(a)
#print(a[1])
#b = mu(a)
#b = map(lambda x: ('expr', ('variable', (x[0].data, ('attrib', x[1].data)))), a)
print(p.parse())