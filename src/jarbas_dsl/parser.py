import sys
import ox
from lexer import tokenize, valid_tokens
from collections import namedtuple


Var = namedtuple('Var', 'id')
Func = namedtuple('Func', 'id args')
Attr = namedtuple('Attr', 'id belongs_to')
Method = namedtuple('Method', 'id belongs_to args')
Filter = namedtuple('Filter', 'id')
Expr = namedtuple('Expr', 'components')
Text = namedtuple('Text', 'value')
Num = namedtuple('Num', 'value')
Bool = namedtuple('Bool', 'value')
Str = namedtuple('Str', 'value')
Input = namedtuple('Input', 'save_in type default validate_func')
Conditional = namedtuple('Condtional', 'type condition')
Comment = namedtuple('Comment', 'value')


# Arguments of a method must be separated
# by a single comma in the format "method(arg1,arg2)"
# or "method(arg1, arg2)", any other format will result
# in a method with args = None
def multi_arg(arg1, text, arg2):
    if text.replace(' ', '') == ',':
        return [arg1] + arg2


# Input
def normal_input(bracket_open, variable, bracket_close):
    return Input(save_in=variable,
                 type=None, default=None, validate_func=None)

def type_input(bracket_open, variable, eq, t, bracket_close):
    return Input(save_in=variable,
                 type=t, default=None, validate_func=None)


def default_input(bracket_open, variable, at, d, bracket_close):
    return Input(save_in=variable,
                 type=None, default=d, validate_func=None)


def validated_input(bracket_open, variable, ap, f, bracket_close):
    return Input(save_in=variable,
                 type=None, default=None, validate_func=f)


# Variables
def variable(id):
    return Var(id.replace('$', ''))


# Attributes
def attribute(var, attr):
    return Attr(id=attr.replace('.', ''), belongs_to=var)


# Functions
def no_args_func(var, p_o, p_c):
    return Func(var.id, None)


def args_func(var, p_o, args, p_c):
    return Func(var.id, args)


# Methods
def no_args_method(var, method, p_o, p_c):
    return Method(method.replace('.', ''), var, None)


def args_method(var, method, p_o, args, p_c):
    return Method(method.replace('.', ''), var, args)


# Filter
def filter(id):
    return Filter(id.replace('|', ''))


parser_rules = [
    ('expr : expr expr', lambda x, y: Expr(components=[x, y])),
    ('expr : utility', lambda x: x),
    ('utility : variable ATTRIB PAREN_O PAREN_C', no_args_method),
    ('utility : variable ATTRIB PAREN_O args PAREN_C', args_method),
    ('utility : variable PAREN_O PAREN_C', no_args_func),
    ('utility : variable PAREN_O args PAREN_C', args_func),
    ('utility : variable', lambda x: x),
    ('utility : PIPE_FILTER', filter),
    ('utility : BRACKET_O variable BRACKET_C', normal_input),
    ('utility : BRACKET_O variable EQUAL TEXT BRACKET_C', type_input),
    ('utility : BRACKET_O variable AT TEXT BRACKET_C', default_input),
    ('utility : BRACKET_O variable AMPER TEXT BRACKET_C', validated_input),
    ('args : arg TEXT args', multi_arg),
    ('args : arg', lambda token: [token]),
    ('expr : text', lambda x: x),
    ('expr : comment', lambda x: x),
    ('variable : variable ATTRIB', attribute),
    ('variable : VARIABLE', variable),
    ('arg : variable', lambda x: x),
    ('arg : NUMBER', lambda token: Num(value=token)),
    ('arg : BOOLEAN', lambda token: Bool(value=token)),
    ('arg : STRING', lambda token: Str(value=token.replace("'", ''))),
    ('text : TEXT', lambda token: Text(value=token)),
    ('comment : COMMENT', lambda token: Comment(value=token)),
]

parser = ox.make_parser(parser_rules, valid_tokens)


class Parser(object):
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


var_name = "Hello $m.is_minor($person.age, True)"
p = Parser(var_name)
#a = p.test()
#print(a)
#print(a[1])
#b = mu(a)
#b = map(lambda x: ('expr', ('variable', (x[0].data, ('attrib', x[1].data)))), a)
print(p.parse())
