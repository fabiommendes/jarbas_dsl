import pytest
import jarbas_dsl
from jarbas_dsl.parser import Parser


@pytest.fixture
def test_parser(test_string):
    return str(Parser(test_string).parse())


def test_method():
    string = "$m.is_minor($person.age, True)"
    expected = ("Method(id='is_minor', belongs_to=Var(id='m'), args=[Attr(id='age', belongs_to=Var(id='person')), Bool(value='True')])")

    assert test_parser(string) == expected


def test_input_without_default():
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


def test_string_without_function():
    string = "'振深面作果品選学我岐縦'"
    try:
        test_parser(string)
    except(SyntaxError):
        assert True


def test_chinese_text():
    string = "振深面作果品選学我岐縦判裁見。出位改購覇野告公料愛芸生多提係属。経最康覧政料区総栗様気投無種警込。中介注社保道験爆夏保逃聞気畑心全名買部。滑広光階芸座発態文指議球立度驚"

    expected = "Text(value='振深面作果品選学我岐縦判裁見。出位改購覇野告公料愛芸生多提係属。経最康覧政料区総栗様気投無種警込。中介注社保道験爆夏保逃聞気畑心全名買部。滑広光階芸座発態文指議球立度驚')"
    assert test_parser(string) == expected


def test_string_with_function():
    string = "振深面作果品選学我$function('出位改購覇野提係属。経最康様気投無種警込。')広光階芸座発議球立度驚"

    expected = "Expr(components=[Text(value='振深面作果品選学我'), Expr(components=[Func(id='function', args=[Str(value='出位改購覇野提係属。経最康様気投無種警込。')]), Text(value='広光階芸座発議球立度驚')])])"
    assert test_parser(string) == expected


def test_validate_func():
    string = "$validate_user($username)"

    expected = "Func(id='validate_user', args=[Var(id='username')])"
    assert test_parser(string) == expected
