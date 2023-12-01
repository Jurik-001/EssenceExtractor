from pydantic import BaseModel, HttpUrl, validator
import re

class YouTubeURL(BaseModel):
    url: HttpUrl

    @validator('url')
    def validate_youtube_url(cls, v):
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
