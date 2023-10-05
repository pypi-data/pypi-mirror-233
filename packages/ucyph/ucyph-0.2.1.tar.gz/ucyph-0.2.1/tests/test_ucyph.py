from unittest.mock import patch, call
from src.ucyph.ucyph import interactive_mode


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_mode(mock_print, mock_input):
    mock_input.side_effect = ['3', 'Hello', 'e', 'n']
    interactive_mode()
    mock_print.assert_has_calls([call("The encrypted text is: khoor")])


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_mode_with_key(mock_print, mock_input):
    mock_input.side_effect = ['5', 'Hello', 'mypassword', 'e', 'n']
    interactive_mode()
    mock_print.assert_has_calls([call("The encrypted text is: tcalg")])


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_mode_invalid_usage_code(mock_print, mock_input):
    mock_input.side_effect = ['100', KeyboardInterrupt]
    interactive_mode()
    mock_print.assert_has_calls([call("Invalid usage code.")])
