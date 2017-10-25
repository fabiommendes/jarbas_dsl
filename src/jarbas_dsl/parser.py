import ox
from lexer import tokenize
from collections import namedtuple

class Parser:
    """
    Parse a string of Jarbas DSL code. 
    
    It creates an AST object which is returned by the Parser.parse() method.
    """
    def number(token):
        return float(token.data)

    def variable(token):
        Var = namedtuple('Var', 'id')
        return Var(id=token.data.replace('$', ''))

    def attribute(token):
        Attr = namedtuple('Atrr', 'id')
        return Attr(id=token.data.replace('.', ''))

    def expr_attrib(v, a):
        Expr = namedtuple('Expr', 'variable attrib')
        return Expr(variable=v, attrib=a)

    parser_rules = [
        ('expr : var attr', expr_attrib),
        ('attr : ATTRIB', attribute),
        ('var  : VARIABLE', variable),
        ('atom : NUMBER', number),
    ]

    def __init__(self, source):
        self.source = source
        self.tokens = tokenize(source)
        print(type(self.tokens[0]))

    def parse(self):
        """
        Parse input source code and return a Jarbas DSL AST.
        """
        return ox.make_parser(self.parser_rules, self.tokens)
        #raise NotImplementedError

    def test(self):
        return self.tokens

s = '$person.name'
p = Parser(s)
#a = p.test()
#print(a)
#print(a[1])
#b = mu(a)
#b = map(lambda x: ('expr', ('variable', (x[0].data, ('attrib', x[1].data)))), a)
print(p.parse())