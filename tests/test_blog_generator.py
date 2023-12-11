from unittest.mock import MagicMock
import pytest
from essence_extractor import BlogGenerator
from pydantic import ValidationError
from tempfile import NamedTemporaryFile
import os


def test_read_text_file(monkeypatch):
    monkeypatch.setattr('src.blog_generator.OpenAI', MagicMock())
    monkeypatch.setattr('src.utils.TokenCounter', MagicMock())

    blog_generator = BlogGenerator()

    with NamedTemporaryFile(delete=False, mode="w") as tmp_file:
        tmp_file.write("Sample content for testing")
        tmp_file_name = tmp_file.name

    text = blog_generator._read_text_file(tmp_file_name)

    assert text == "Sample content for testing", "The content read does not match the expected content"

    os.remove(tmp_file_name)

    with pytest.raises(ValidationError):
        blog_generator._read_text_file('non_existent_file_path')


def test_split_into_first_chunk(monkeypatch):
    def mock_count_tokens(self, text):
        return len(text.split())

    monkeypatch.setattr('src.blog_generator.OpenAI', MagicMock())
    monkeypatch.setattr('src.utils.TokenCounter.count_tokens', mock_count_tokens)

    generator = BlogGenerator()

    text = "This is a test sentence for testing."
    chunk_size = 4

    chunk = generator._split_into_first_chunk(text, chunk_size)

    expected_chunk = "This is a test"
    assert chunk == expected_chunk, "The chunked text does not match the expected output"

