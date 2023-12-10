"""Download a YouTube video."""

import os

from pytube import YouTube

from essence_extractor.src import utils
from essence_extractor.src.data_models import YouTubeURL


class YouTubeDownloader:
    """Download a YouTube video.

    Attributes:
        output_path (str): The path to the output directory.
    """
    def __init__(self, output_path="videos"):
        self.output_path = output_path
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def download_video(self, url):
        """Download a YouTube video.

        Args:
            url (str): The URL of the YouTube video.

        Returns:
            str: The path to the downloaded video file.
        """
        url = str(YouTubeURL(url=url).url)
        try:
            yt = YouTube(url)

            ys = yt.streams.get_highest_resolution()

            video_file_path = os.path.join(self.output_path, ys.default_filename)

            ys.download(self.output_path)
            return video_file_path

        except Exception as e:
            raise utils.YouTubeDownloadError(f"Error downloading YouTube video: {e}")
