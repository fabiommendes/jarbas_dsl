import ox
from lexer import tokenize, valid_tokens
from collections import namedtuple


Var = namedtuple('Var', 'id')
Attr = namedtuple('Attr', 'id')
Method = namedtuple('Method', 'id params')
Expr = namedtuple('Expr', 'args')

def number(token):
    return float(token)

def variable(token):
    return Var(id=token.replace('$', ''))

def attribute(token):
    return Attr(id=token.replace('.', ''))

def method_params(a, po, params, pc):
    return Method(a.replace('.', ''), params)

def method_noparams(a, po, pc):
    return Method(a.replace('.', ''), None)


def expr_attrib(v, a):
    return Expr((v, a))

def expr_method(e, m):
    return Expr((e, m))

parser_rules = [
    ('expr : expr method', expr_method),
    ('expr : expr attr', expr_attrib),
    ('expr : var', lambda x: x),
    ('method : ATTRIB PAREN_O num PAREN_C', method_params),
    ('method : ATTRIB PAREN_O PAREN_C', method_noparams),
    ('attr : ATTRIB', attribute),
    ('var  : VARIABLE', variable),
    ('num : NUMBER', number),
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

s = '$person.title()'
p = Parser(s)
#a = p.test()
#print(a)
#print(a[1])
#b = mu(a)
#b = map(lambda x: ('expr', ('variable', (x[0].data, ('attrib', x[1].data)))), a)
print(p.parse())