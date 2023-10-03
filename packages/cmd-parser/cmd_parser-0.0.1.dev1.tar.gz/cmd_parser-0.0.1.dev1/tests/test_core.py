import pytest

from cmd_parser.core import asdict, parse


class TestParser:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.command = '!command arg1 arg2 param1=value1 param2=value2'

    def test_given_command_as_input_it_should_return_5_tokens(self):
        input_test = len(list(parse(self.command)))
        expected = 5
        assert input_test, expected

    def test_given_command_as_input_it_should_return_a_dict(self):
        result = asdict(parse(self.command))
        expected = {
            'command': 'command',
            'args': ['arg1', 'arg2'],
            'kwargs': {'param1': 'value1', 'param2': 'value2'},
        }
        assert result, expected


@pytest.mark.parametrize(
    'input_test,expected',
    [
        ('param="value', 'No closing quotation'),
        ('.', "No handler for the token -> '.'"),
        ('-', "No handler for the token -> '-'"),
        # ('1', "No handler for the token -> '1'"),
        # (' ', "??"), # TODO
        # ('', "??"), # TODO
        # (0, "??"), # TODO
    ],
)
def test_should_catch_value_erro_exception_for_malformed_inputs(
    input_test, expected
):
    with pytest.raises(expected_exception=ValueError, match=expected) as exc:
        asdict(parse(input_test))
    assert str(exc.value) == expected
