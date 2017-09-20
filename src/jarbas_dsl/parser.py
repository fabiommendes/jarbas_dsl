class Parser:
    """
    Parse a string of Jarbas DSL code. 
    
    It creates an AST object which is returned by the Parser.parser() method.
    """

    def __init__(self, source):
        self.source = source

    def parse(self):
        """
        Parse input source code and return a Jarbas DSL AST.
        """
        raise NotImplementedError
