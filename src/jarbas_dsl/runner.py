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
 
        input_act = None
        output_line = ''
        has_input = False

        for action in self.ast.components:

            if isinstance(action, Text):
               output_line += action.value

            elif isinstance(action, Var):
                try:
                    attr = getattr(namespace, action.id)
                    output_line += attr
                except AttributeError:
                    raise ValueError("ariable %s not defined" % action.id)

            elif isinstance(action, Attr):
                try:
                    attr = namespace.get_attr_with_path(action.path)
                    output_line += attr
                except AttributeError:
                    raise ValueError("attribute %s not defined" % action.path)

            elif isinstance(action, Input):
                has_input = True
                try:
                    attr = namespace.get_attr_with_path(action.save_in)
                    raw_data = input(output_line)

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
                        namespace.set_attr_with_path(action.save_in, raw_data)
                except AttributeError:
                    pass
                    
                    #raise ValueError("Variable or Attribute %s or Filter %s doesn't exist" % (action.save_in, action.filter))
        
        if not has_input:
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



s = 'What is your name? [person.name]\n\nHello $person.name'
f = open('./input_file.jb')
p = parse(f.read())
r = Runner(p)
r.run({'person': {'name': ''}})