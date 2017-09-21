import ox


class Lexer:

    def __init__(self):
        self.token_list = ['TEXT', 'VARIABLE', 'POINT', 'PIPE',
                           'COMMENT_MARKER', 'PARENTHESES_O', 'PARENTHESES_C']

        self.lexer = ox.make_lexer([
            (self.token_list[0], r'[a-zA-Z_0-9!@#?%&*]+'),
            (self.token_list[1], r'\$[a-zA-Z]([a-zA-Z0-9_]*)'),
            (self.token_list[2], r'\.'),
            (self.token_list[3], r'\|'),
            (self.token_list[4], r'//'),
            (self.token_list[5], r'\('),
            (self.token_list[6], r'\)')
        ])

    # Token list to be used on Parser
    def get_token_list(self):
        return self.token_list

    # Create a list of tokens based on lexer rules and text passed as string
    def generate_tokens(self, string):
        return self.lexer(string)
