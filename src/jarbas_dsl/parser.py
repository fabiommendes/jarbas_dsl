import sys
import ox
from lexer import tokenize, valid_tokens
from collections import namedtuple


Var = namedtuple('Var', 'id')
Attr = namedtuple('Attr', 'id')
Method = namedtuple('Method', 'id args')
Expr = namedtuple('Expr', 'components')
Text = namedtuple('Text', 'value')
Num = namedtuple('Num', 'value')
Bool = namedtuple('Bool', 'value')
Str = namedtuple('Str', 'value')


# Arguments of a method must be separated
# by a single comma in the format "method(arg1,arg2)"
# or "method(arg1, arg2)", any other format will result
# in a method with args = None
def multi_arg(arg1, text, arg2):
    if text == ', ' or text == ',':
        args = [arg1, arg2]
        return args

parser_rules = [
    ('expr : expr expr', lambda x,y : Expr(components=[x, y])),
    ('expr : access', lambda x: x),
    ('access : ATTRIB PAREN_O PAREN_C', lambda m, p_o, p_c : Method(m.replace('.', ''), None)),
    ('access : ATTRIB PAREN_O args PAREN_C', lambda m, p_o, a, p_c : Method(m.replace('.', ''), a)),
    ('access : ATTRIB', lambda token : Attr(id=token.replace('.', ''))),
    ('access : VARIABLE', lambda token : Var(id=token.replace('$', ''))),
    ('args : arg TEXT args', multi_arg),
    ('args : arg', lambda token : token),
    ('expr : text', lambda x: x),
    ('arg : NUMBER', lambda token : Num(value=token)),
    ('arg : BOOLEAN', lambda token : Bool(value=token)),
    ('arg : STRING', lambda token : Str(value=token.replace("'", ''))),
    ('text : TEXT', lambda token : Text(value=token)),
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

    def parse(self):
        """
        Parse input source code and return a Jarbas DSL AST.
        """
        return parser(self.tokens)

s = "Hello $person.title(True,2)"
#s = "."
p = Parser(s)
#a = p.test()
#print(a)
#print(a[1])
#b = mu(a)
#b = map(lambda x: ('expr', ('variable', (x[0].data, ('attrib', x[1].data)))), a)
print(p.parse())