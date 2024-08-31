import pytest
from unittest.mock import patch, MagicMock
from src.cli import cli
from src.scriptomatic import Scriptomatic

MODEL = "gpt-4o-mini"
@pytest.fixture
def mock_scriptomatic():
    with patch('src.cli.Scriptomatic') as mock:
        yield mock

@pytest.fixture
def mock_argparse():
    with patch('src.cli.argparse.ArgumentParser') as mock:
        yield mock

def test_cli_with_prompt(mock_scriptomatic, mock_argparse):
    mock_args = MagicMock(prompt="Test prompt", loop=False, inspo=False, autoloop=False, model=MODEL, temperature=0.2)
    mock_argparse.return_value.parse_args.return_value = mock_args

    cli()

    mock_scriptomatic.assert_called_once_with(model=MODEL, temperature=0.2)
    mock_scriptomatic.return_value.generate_script.assert_called_once_with("Test prompt", loop=False, autoloop=False)

def test_cli_with_inspo(mock_scriptomatic, mock_argparse):
    mock_args = MagicMock(prompt=None, loop=False, inspo=True, autoloop=False, model=MODEL, temperature=0.2)
    mock_argparse.return_value.parse_args.return_value = mock_args
    mock_scriptomatic.return_value.get_inspiration.return_value = "Inspired prompt"

    cli()

    mock_scriptomatic.assert_called_once_with(model=MODEL, temperature=0.2)
    mock_scriptomatic.return_value.get_inspiration.assert_called_once()
    mock_scriptomatic.return_value.generate_script.assert_called_once_with("Inspired prompt", loop=False, autoloop=False)

def test_cli_with_loop(mock_scriptomatic, mock_argparse):
    mock_args = MagicMock(prompt="Test prompt", loop=True, inspo=False, autoloop=False, model=MODEL, temperature=0.2)
    mock_argparse.return_value.parse_args.return_value = mock_args

    cli()

    mock_scriptomatic.assert_called_once_with(model=MODEL, temperature=0.2)
    mock_scriptomatic.return_value.generate_script.assert_called_once_with("Test prompt", loop=True, autoloop=False)


def test_cli_without_prompt_or_inspo(mock_scriptomatic, mock_argparse, capsys):
    mock_args = MagicMock(prompt=None, loop=False, inspo=False, autoloop=False, model=MODEL, temperature=0.2)
    mock_argparse.return_value.parse_args.return_value = mock_args

    cli()

    captured = capsys.readouterr()
    assert "Please provide a prompt or use --inspo for inspiration mode." in captured.out
    mock_scriptomatic.return_value.generate_script.assert_not_called()