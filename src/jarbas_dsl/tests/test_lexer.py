import pytest
import jarbas_dsl
from jarbas_dsl.lexer import tokenize


@pytest.fixture
def test_lexer(string,expected):
    tokenized_source_list = tokenize(string)
    token_values_list = []
    for token in tokenized_source_list:
        token_values_list.append(token.value)
    assert token_values_list == expected


# Tests of dollar sign small transformations and comments
def test_lexer_attribute_access():
    string = "Hello $person.name!"
    expected = ["Hello ", "$person", ".name", "!"]
    test_lexer(string, expected)

def test_lexer_method_calling():
    string = "Hello $name.title()!"
    expected = ["Hello ", "$name", ".title", "(", ")", "!"]
    test_lexer(string, expected)

def test_pipe_operator():
    string = "Hello $name|title!"
    expected = ["Hello ", "$name", "|title", "!"]
    test_lexer(string, expected)

def test_comment():
    string = "Hello $person.name! // attribute access"
    expected = ["Hello ", "$person", ".name", "! ", "// attribute access"]
    test_lexer(string, expected)


# Tests of user input token
def test_simple_user_input():
    string = "Name: [name] Hello $name!"
    expected = ["Name: ", "[", "name", "]", " Hello ", "$name", "!"]
    test_lexer(string, expected)

def test_defined_type_user_input():
    string = "Name: [age=int] Hello $name!"
    expected = ["Name: ", "[", "age", "=", "int", "]", " Hello ", "$name", "!"]
    test_lexer(string, expected)

def test_function_validation_user_input():
    string = "Name: [email=&email] Hello $name!"
    expected = ["Name: ", "[", "email", "=&", "email", "]", " Hello ", "$name", "!"]
    test_lexer(string, expected)

def test_default_value_user_input():
    string = "Name: [github=@email] Hello $name!"
    expected = ["Name: ", "[", "github", "=@", "email", "]", " Hello ", "$name", "!"]
    test_lexer(string, expected)


# Test of multiple lines source code
def test_lexer_multiple_lines():
    string = "Name: [name] //comment here\n Hello $name.title()!"
    expected = ["Name: ", "[", "name","]", " ", "//comment here", "\n Hello ",
                "$name", ".title", "(", ")", "!"]
    test_lexer(string,expected)


# Tests of conditional execution
def test_lexer_if_conditional():
    string = "=if $condition"
    expected = ["=if ", "$condition"]
    test_lexer(string,expected)

def test_lexer_elif_conditional():
    string = "=elif Do you want to proceed? [proceed=bool]"
    expected = ["=elif ", "Do you want to proceed? ", "[", "proceed", "=", "bool", "]"]
    test_lexer(string,expected)

def test_lexer_else_conditional():
    string = "=else \n"
    expected = ["=", "else \n"]
    test_lexer(string,expected)

def test_lexer_all_conditionals():
    string = "=if $is_minor(age)\nYou cannot proceed.\n=elif Do you want to proceed?\
 [proceed=bool]\nOk, let's go!\n=else\nBye!\n=endif"
    expected = ["=if ", "$is_minor", "(", "age", ")", "\nYou cannot proceed.\n", "=elif ",
                "Do you want to proceed? ", "[", "proceed", "=", "bool", "]", "\nOk, let's go!\n",
                "=else\n", "Bye!\n", "=endif"]
    test_lexer(string,expected)
