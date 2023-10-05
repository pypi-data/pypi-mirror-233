from __future__ import annotations

from unittest.mock import Mock

import pytest

from pymarks import cli


@pytest.fixture
def mock_cursor():
    return Mock(name="Cursor")

@pytest.fixture
def mock_clipboard_url():
    return "https://example.com"

@pytest.fixture
def mock_title_and_description():
    return "Example Title", "Example Description"

def test_add_with_valid_url(mock_cursor, mock_clipboard_url, mock_title_and_description, mocker):  # noqa: E501
    mocker.patch("utils.read_from_clipboard", return_value=mock_clipboard_url)
    mocker.patch("prompt_toolkit.prompt", side_effect=["https://example.com", "tag1,tag2"])  # noqa: E501
    mocker.patch("scrape.title_and_description", return_value=mock_title_and_description)  # noqa: E501
    mocker.patch("prompt_toolkit.confirm", return_value=True)
    mocker.patch("database.create_bookmark", return_value=Mock(id=1))

    cli.add(mock_cursor)

    # Add your assertions here based on the expected behavior

def test_add_with_empty_url(mock_cursor, mocker):
    mocker.patch("utils.read_from_clipboard", return_value="")
    mocker.patch("prompt_toolkit.prompt", return_value="")
    mocker.patch("console.print")

    cli.add(mock_cursor)

    # Add your assertions here based on the expected behavior

if __name__ == "__main__":
    pytest.main()
