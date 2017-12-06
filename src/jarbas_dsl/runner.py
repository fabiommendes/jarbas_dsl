import collections
from namespace import Namespace
from parser import Text, Var, Attr, parse


class Runner:
    """
    Execute a parsed Jarbas AST.
    """

    def __init__(self, ast, filters=None, validators=None):
        self.ast = ast
        self.filters = dict(filters or {})
        self.validators = dict(validators or {})

    def run(self, namespace=None):
        """
        Run interaction in the given namespace.
        """

        namespace = normalize_namespace(namespace)
 
        output_line = ''
        input_act = None

        for action in self.ast.components:
            if isinstance(action, Text):
               output_line += action.value

            elif isinstance(action, Var):
                try:
                    var = getattr(namespace, action.id)
                    output_line += var
                except AttributeError:
                    raise NotImplementedError

            elif isinstance(action, Attr):
                try:
                    attr = namespace.get_attr_with_path(action.path)
                    output_line += attr
                except AttributeError:
                    raise NotImplementedError

        print(output_line)

def normalize_namespace(namespace):
    """
    Normalize namespace entry.
    """

    if namespace is None:
        return Namespace()
    elif isinstance(namespace, collections.Mapping):
        return Namespace(namespace)
    else:
        return namespace


s = 'Hello $person.name!'
p = parse(s)
r = Runner(p)
r.run({'person': {'name': 'Agnaldo'}})