from .parser import Parser
from .runner import Runner


def run_code(source, namespace=None, filters=None, validators=None):
    """
    Run a piece of code using the Jarbas DSL.

    Args:
        source:
            A string of Jarbas DSL source.
        namespace:
            A namespace dictionary or a Python object that accepts getattr and
            setattr. It can be pre-populated with variables and functions. 
        filters:
            A dictionary mapping filter names to filter functions.
        validators:
            A dictionary mapping validator names to validator functions.
    """

    # Parse code
    parser = Parser(source)
    ast = parser.parse()

    # Run it in the given namespace
    runner = Runner(ast, filters=filters, validators=validators)
    runner.run(namespace)
