import pytest
import jarbas_dsl
from jarbas_dsl.lexer import tokenize

def test_project_defines_author_and_version():
    assert hasattr(jarbas_dsl, '__author__')
    assert hasattr(jarbas_dsl, '__version__')

@pytest.fixture
def test_lexer(string,expected):
    tokenized_source = tokenize(string)
    assert tokenized_source == expected

def test_lexer_method_calling():
    string = "Hello $name.title()!    // method calling"
    expected = ["Hello ", "$name", ".title", "(", ")", "!    ", "// method calling"]
    test_lexer(string, expected)

def test_lexer_multiple_lines():
    string = "Name: [name] //comment here\n Hello $name.title()!"
    expected = ["Name: ", "[", "name","]", " ", "//comment here", "\n Hello ",
                "$name", ".title", "(", ")", "!"]
    test_lexer(string,expected)


def test_lexer_if_calling():
    string = "=if $condition"
    expected = ["=", "if $condition"]
    test_lexer(string,expected)
