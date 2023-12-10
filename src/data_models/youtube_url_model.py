"""Data model for YouTube URL."""

import re

from pydantic import BaseModel, HttpUrl, validator


class YouTubeURL(BaseModel):
    """Data model for YouTube URL."""
    url: HttpUrl

    @validator('url')
    def validate_youtube_url(cls, v):
        """Validate that the URL is a valid YouTube URL."""
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        url_str = str(v)

        if not re.match(youtube_regex, url_str):
            raise ValueError('Invalid YouTube URL')
        if 't=' in url_str:
            raise ValueError('URL contains timestamp, please remove the timestamp')
        return v
