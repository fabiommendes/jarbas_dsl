import sys
import ox
from lexer import tokenize, valid_tokens
from collections import namedtuple


Var = namedtuple('Var', 'id')
Attr = namedtuple('Attr', 'path')
Filter = namedtuple('Filter', 'target filter')
Expr = namedtuple('Expr', 'components')
Text = namedtuple('Text', 'value')
Input = namedtuple('Input', 'save_in type default validate_func')
Conditional = namedtuple('Condtional', 'type condition text')


# Input
def normal_input(s_input, name1, e_input):
    return Input(save_in=name1,
                 type=None, default=None, validate_func=None)

def type_input(s_input, name1, eq, name2, e_input):
    return Input(save_in=name1,
                 type=name2, default=None, validate_func=None)


def default_input(s_input, name1, at, name2, e_input):
    return Input(save_in=name1,
                 type=None, default=name2, validate_func=None)


def validated_input(s_input, name1, amper, name2, e_input):
    return Input(save_in=name1,
                 type=None, default=None, validate_func=name2)


# Chained attributes e.g. var.attr1.attr2
def output_chained_attr(var, attributes):
    path = var.id
    for a in attributes:
        path += a
    return Attr(path = path)


# Filter
def var_filter(var, pipe, filter):
    return Filter(target = var.id, filter = filter)

def attr_filter(attr, pipe, filter):
    return Filter(target = attr.path, filter = filter)


# Conditional
def simple_conditional(x, y, z):
    condition_type = 'simple_' + x[1:]
    return Conditional(type=condition_type, condition=y, text=None)

def output_conditional(t, o, c, z):
    condition_type = 'output_' + t.split('=')[1]
    return Conditional(type=condition_type, condition=c, text=o.value)

parser_rules = [
    ('expr : expr utility', lambda x, y: Expr(components = x.components + [y])),
    ('expr : utility', lambda x: Expr(components = [x])),
    #('expr : conditional' , lambda x: Expr(components = [x])),
    #('conditional : SIMPLE_ELSE', output_conditional),                
    # ('conditional : OUTPUT_ELIF text input END_CONTROL', output_conditional),
    # ('conditional : SIMPLE_ELIF output_var END_CONTROL', simple_conditional),
    # ('conditional : OUTPUT_IF text input END_CONTROL', output_conditional),
    # ('conditional : SIMPLE_IF output_var END_CONTROL', simple_conditional),
    ('utility : filter', lambda x: x),        
    ('utility : input', lambda x: x),        
    ('utility : output_attr', lambda x: x),    
    ('utility : output_var', lambda x: x),
    ('utility : text', lambda x: x),
    ('filter : output_attr PIPE_FILTER NAME', attr_filter),
    ('filter : output_var PIPE_FILTER NAME', var_filter),
    ('input : START_INPUT NAME END_INPUT', normal_input),
    ('input : START_INPUT NAME EQUAL NAME END_INPUT', type_input),
    ('input : START_INPUT NAME AT NAME END_INPUT', default_input),
    ('input : START_INPUT NAME AMPER NAME END_INPUT', validated_input),
    ('output_attr : output_var chained_attr', output_chained_attr),
    ('output_attr : output_var OUTPUT_ATTR', lambda x, y: Attr(path = x.id + y)),
    ('output_var : OUTPUT_VAR', lambda x: Var(id = x[1:])),
    ('chained_attr : chained_attr OUTPUT_ATTR', lambda x, y: x + [y]),
    ('chained_attr : OUTPUT_ATTR OUTPUT_ATTR', lambda x, y: [x] + [y]),
    ('text : TEXT', lambda token: Text(value = token)),
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

    def parse(self):
        """
        Parse input source code and return a Jarbas DSL AST.
        """
        return parser(self.tokens)


def parse(src):
    p = Parser(src)
    return p.parse()
