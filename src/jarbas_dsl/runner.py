import collections

from .namespace import Namespace


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
        raise NotImplementedError


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
