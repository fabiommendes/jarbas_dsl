import sys
import ox
from lexer import tokenize, valid_tokens
from collections import namedtuple


Var = namedtuple('Var', 'id')
Func = namedtuple('Func', 'id args')
Attr = namedtuple('Attr', 'id belong_to')
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

# Input
def normal_input(b_o, s, b_c):
    return Input(save_in=s, type=None, default=None, validate_func=None)

def type_input(b_o, s, eq, t, b_c):
    return Input(save_in=s, type=t, default=None, validate_func=None)

def default_input(b_o, s, eq, at, d, b_c):
    return Input(save_in=s, type=None, default=d, validate_func=None)

def validated_input(b_o, s, eq, ap, f, b_c):
    return Input(save_in=s, type=None, default=None, validate_func=f)


# Variables
def variable(id):
    return Var(id.replace('$', ''))

# Attributes
def attribute(var, attr):
    return Attr(attr.replace('.', ''), var.replace('$', ''))

# Functions
def no_args_func(id, p_o, p_c):
    return Func(id.replace('$', ''), None)

def args_func(id, p_o, args, p_c):
    return Func(id.replace('$', ''), args)

# Methods
def no_args_method(id, p_o, p_c):
    return Func(id.replace('.', ''), None)

def args_method(id, p_o, args, p_c):
    return Func(id.replace('.', ''), args)
    
# Filter
def filter(id):
    return Filter(id.replace('|', ''))

parser_rules = [
    ('expr : expr expr', lambda x,y : Expr(components=[x, y])),
    ('expr : utility', lambda x: x),
    ('utility : ATTRIB PAREN_O PAREN_C', no_args_method),
    ('utility : ATTRIB PAREN_O args PAREN_C', args_method),
    ('utility : VARIABLE PAREN_O PAREN_C', no_args_func),
    ('utility : VARIABLE PAREN_O args PAREN_C', args_func),
    ('utility : VARIABLE ATTRIB', attribute),
    ('utility : VARIABLE', variable),
    ('utility : PIPE_FILTER', filter),
    ('utility : BRACKET_O TEXT BRACKET_C', normal_input),
    ('utility : BRACKET_O TEXT EQUAL TEXT BRACKET_C', type_input),
    ('utility : BRACKET_O TEXT EQUAL AT TEXT BRACKET_C', default_input),
    ('utility : BRACKET_O TEXT EQUAL AMPER TEXT BRACKET_C', validated_input),
    ('args : arg TEXT args', multi_arg),
    ('args : arg', lambda token : token),
    ('expr : text', lambda x: x),
    ('expr : comment', lambda x: x),
    ('arg : VARIABLE', variable),
    ('arg : VARIABLE ATTRIB', attribute),
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
        print(self.tokens)

    def parse(self):
        """
        Parse input source code and return a Jarbas DSL AST.
        """
        return parser(self.tokens)

s = "$is_minor($age.name)"
#s = "=if $is_minor($age)"
p = Parser(s)
#a = p.test()
#print(a)
#print(a[1])
#b = mu(a)
#b = map(lambda x: ('expr', ('variable', (x[0].data, ('attrib', x[1].data)))), a)
print(p.parse())