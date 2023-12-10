# tests/test_youtube_url_model.py
import pytest
from src.data_models import YouTubeURL
from pydantic import ValidationError


def test_valid_youtube_url():
    valid_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
    ]
    for url in valid_urls:
        try:
            YouTubeURL(url=url)
        except Exception as e:
            pytest.fail(f"URL {url} should be valid")


def test_youtube_url_with_timestamp():
    url_with_timestamp = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s"
    with pytest.raises(ValidationError):
        YouTubeURL(url=url_with_timestamp)


def test_invalid_youtube_url():
    invalid_urls = [
        "https://www.example.com/watch?v=dQw4w9WgXcQ",
    ]
    for url in invalid_urls:
        with pytest.raises(ValidationError):
            YouTubeURL(url=url)
