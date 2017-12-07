import collections
from namespace import Namespace
from parser import Text, Var, Attr, Filter, Input, parse


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

        for action in self.ast.components:

            if isinstance(action, Text):
                print(action.value, end="")
            elif isinstance(action, Var):
                try:
                    attr = getattr(namespace, action.id)
                    print(attr, end="")
                except AttributeError:
                    raise ValueError("ariable %s not defined" % action.id)

            elif isinstance(action, Attr):
                try:
                    attr = namespace.get_attr(action.path)
                    print(attr, end="")
                except AttributeError:
                    raise ValueError("attribute %s not defined" % action.path)

            elif isinstance(action, Input):
                try:
                    raw_data = input()

                    if action.type:
                        if action.type == 'int':
                            try:
                                input_data = int(raw_data)
                            except ValueError:
                                raise ValueError("Value of invalid type %s" % raw_data)
                        elif action.type == 'bool':
                            if raw_data == 'True':
                                input_data = True
                            elif raw_data == 'False':
                                input_data = False
                            else:
                                raise ValueError("Value of invalid type %s" % raw_data)
                        else:
                            raise ValueError("Invalid type %s" % action.type)
                    
                    elif action.default:
                        pass
                    elif action.validate_func:
                        pass
                    else:
                        namespace.set_value(action.save_in, raw_data)
                except AttributeError:
                    raise AttributeError(raw_data)
                    
                    #raise ValueError("Variable or Attribute %s or Filter %s doesn't exist" % (action.save_in, action.filter))


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



f = open('./input_file.jb')
p = parse(f.read())
#p = parse(s)
r = Runner(p)
r.run({'person': {'name': 'João', 'age': ''}})