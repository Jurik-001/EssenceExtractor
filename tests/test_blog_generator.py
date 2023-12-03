from unittest.mock import patch, mock_open, MagicMock
import pytest
from src.blog_generator import BlogGenerator

# Mocking OpenAI Client
@patch('src.blog_generator.OpenAI')
def test_generate_answer_with_mocked_openai(mock_openai_client):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0] = [MagicMock(message=MagicMock(content='Mocked response'))]
    mock_openai_client.chat.completions.create.return_value = mock_response

    # Instantiate BlogGenerator and call _generate_answer
    blog_generator = BlogGenerator()
    result = blog_generator._generate_answer("System prompt", "User prompt")

    # Assert the mocked response is returned
    print(f"result: {dir(result)}")
    print(f"Type of result: {type(result)}")
    print()
    assert result == "Mocked response"

# Mocking File Reading
@patch("builtins.open", new_callable=mock_open, read_data="Mocked file content")
def test_read_text_file_with_mocked_file(mock_file):
    # Instantiate BlogGenerator and call _read_text_file
    blog_generator = BlogGenerator()
    content = blog_generator._read_text_file("dummy/path.txt")

    # Assert the mocked file content is returned
    mock_file.assert_called_with("dummy/path.txt", "r")
    assert content == "Mocked file content"


# Test from copilot
# Test when system_prompt is None
@patch('src.blog_generator.OpenAI')
def test_generate_answer_with_none_system_prompt(mock_openai_client):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0] = [MagicMock(message=MagicMock(content='Mocked response'))]
    mock_openai_client.chat.completions.create.return_value = mock_response

    # Instantiate BlogGenerator and call _generate_answer
    blog_generator = BlogGenerator()
    result = blog_generator._generate_answer(None, "User prompt")

    # Assert the mocked response is returned
    assert result == "Mocked response"

# Test when user_prompt is None
@patch('src.blog_generator.OpenAI')
def test_generate_answer_with_none_user_prompt(mock_openai_client):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0] = [MagicMock(message=MagicMock(content='Mocked response'))]
    mock_openai_client.chat.completions.create.return_value = mock_response

    # Instantiate BlogGenerator and call _generate_answer
    blog_generator = BlogGenerator()
    result = blog_generator._generate_answer("System prompt", None)

    # Assert the mocked response is returned
    assert result == "Mocked response"

# Test when both prompts are None
@patch('src.blog_generator.OpenAI')
def test_generate_answer_with_both_prompts_none(mock_openai_client):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0] = [MagicMock(message=MagicMock(content='Mocked response'))]
    mock_openai_client.chat.completions.create.return_value = mock_response

    # Instantiate BlogGenerator and call _generate_answer
    blog_generator = BlogGenerator()
    result = blog_generator._generate_answer(None, None)

    # Assert the mocked response is returned
    assert result == "Mocked response"
