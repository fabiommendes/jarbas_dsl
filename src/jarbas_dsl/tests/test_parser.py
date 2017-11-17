import pytest
import jarbas_dsl
from jarbas_dsl.parser import Parser


@pytest.fixture
def test_parser(test_string):
    return str(Parser(test_string).parse())


"""
=================================
Tests for Inputs
=================================
"""

def test_simple_input():
    string = "[$name]"
    expected = "Input(save_in=Var(id='name'), type=None, default=None, validate_func=None)"

    assert test_parser(string) == expected

def test_input_for_attribute():
    string = "Github: [$person.user]"
    expected = "Expr(components=[Text(value='Github: '), Input(save_in=Attr(id='user', belongs_to=Var(id='person')), type=None, default=None, validate_func=None)])"

    assert test_parser(string) == expected


def test_input_with_default():
    string = "Github: [$person.user=@git_username]"
    expected = "Expr(components=[Text(value='Github: '), Input(save_in=Attr(id='user', belongs_to=Var(id='person')), type=None, default='git_username', validate_func=None)])"

    assert test_parser(string) == expected


def test_input_with_validate():
    string = "Github: [$person.user=&validate_user]"
    expected = "Expr(components=[Text(value='Github: '), Input(save_in=Attr(id='user', belongs_to=Var(id='person')), type=None, default=None, validate_func='validate_user')])"

    assert test_parser(string) == expected


def test_input_with_type():
    string = "Github: [$person.user=string]"
    expected = "Expr(components=[Text(value='Github: '), Input(save_in=Attr(id='user', belongs_to=Var(id='person')), type='string', default=None, validate_func=None)])"

    assert test_parser(string) == expected


"""
=================================
Tests for Texts and Strings
=================================
"""


def test_string_without_function():
    string = "'振深面作果品選学我岐縦'"
    try:
        test_parser(string)
        assert False
    except(SyntaxError):
        assert True

def test_text_with_double_quotes():
    string = '"some quote"'

    expected = "Text(value='\"some quote\"')"
    assert test_parser(string) == expected

def test_text_with_string():
    string = '"Hello" $print(\'New User!\')'

    expected = "Expr(components=[Text(value='\"Hello\" '), Func(id='print', args=[Str(value='New User!')])])"
    assert test_parser(string) == expected


def test_chinese_text():
    string = ("振深面作果品選学我岐縦判裁見。出位改購覇野告公料愛芸生多提係属。" +
              "経最康覧政料区総栗様気投無種警込。中介注社保道験爆夏保逃聞気畑心" +
              "全名買部。滑広光階芸座発態文指議球立度")

    expected = ("Text(value='振深面作果品選学我岐縦判裁見。出位改購覇野告公料" +
                "愛芸生多提係属。経最康覧政料区総栗様気投無種警込。中介注社保道" +
                "験爆夏保逃聞気畑心全名買部。滑広光階芸座発態文指議球立度')")
    assert test_parser(string) == expected


"""
=================================
Tests for Functions and Methods parsing
=================================
"""


def test_func_no_args():
    string = "$validate_user()"
    # Question: should this work?
    expected = "Func(id='validate_user', args=None)"
    assert test_parser(string) == expected


def test_func_with_one_arg():
    string = "$validate_user($username)"

    expected = "Func(id='validate_user', args=[Var(id='username')])"
    assert test_parser(string) == expected


def test_func_with_two_args():
    string = "$validate_user($username, 'token')"

    expected = "Func(id='validate_user', args=[Var(id='username'), Str(value='token')])"
    assert test_parser(string) == expected


def test_function_with_strings():
    string = "振深面作果品選学我$function('出位改購覇野提係属。経最康様気投無種警込。')広光階芸座発議球立度驚"

    expected = "Expr(components=[Text(value='振深面作果品選学我'), Expr(components=[Func(id='function', args=[Str(value='出位改購覇野提係属。経最康様気投無種警込。')]), Text(value='広光階芸座発議球立度驚')])])"
    assert test_parser(string) == expected


def test_method_with_no_args():
    string = "$m.is_minor()"
    expected = ("Method(id='is_minor', belongs_to=Var(id='m'), args=None)")

    assert test_parser(string) == expected


def test_method_with_one_arg():
    string = "$m.is_minor($person.age)"
    expected = ("Method(id='is_minor', belongs_to=Var(id='m'), args=[Attr(id='age', belongs_to=Var(id='person'))])")

    assert test_parser(string) == expected


def test_method_with_two_args():
    string = "$m.is_minor($person.age, True)"
    expected = ("Method(id='is_minor', belongs_to=Var(id='m'), args=[Attr(id='age', belongs_to=Var(id='person')), Bool(value='True')])")

    assert test_parser(string) == expected
