import ox
from lexer import tokenize, token_list
from collections import namedtuple


Var = namedtuple('Var', 'id')
Attr = namedtuple('Attr', 'id')
Expr = namedtuple('Expr', 'variable attrib')

def number(token):
    return float(token)

def variable(token):
    return Var(id=token.replace('$', ''))

def attribute(token):
    return Attr(id=token.replace('.', ''))

def expr_attrib(v, a):
    return Expr(variable=v, attrib=a)

parser_rules = [
    ('expr : var attr', expr_attrib),
    ('attr : ATTRIB', attribute),
    ('var  : VARIABLE', variable),
    ('atom : NUMBER', number),
]

parser = ox.make_parser(parser_rules, token_list)

class Parser:
    """
    Parse a string of Jarbas DSL code. 
    
    It creates an AST object which is returned by the Parser.parse() method.
    """

    def __init__(self, source):
        self.source = source
        self.tokens = tokenize(source)
        print(type(self.tokens[0]))

    def parse(self):
        """
        Parse input source code and return a Jarbas DSL AST.
        """
        return parser(self.tokens)

    def test(self):
        return self.tokens

s = '$person.name'
p = Parser(s)
#print(tokenize(s))
#a = p.test()
#print(a)
#print(a[1])
#b = mu(a)
#b = map(lambda x: ('expr', ('variable', (x[0].data, ('attrib', x[1].data)))), a)
print(p.parse())