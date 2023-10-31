"""Download a YouTube video."""

import os

from pytube import YouTube

from src import utils


class YouTubeDownloader:
    """Download a YouTube video."""

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
        try:
            yt = YouTube(url)

            ys = yt.streams.get_highest_resolution()

            video_file_path = os.path.join(self.output_path, ys.default_filename)

            ys.download(self.output_path)
            utils.logging.info(f"Video downloaded: {video_file_path}")
            return video_file_path

        except Exception as e:
            utils.logging.info("An error occurred:", str(e))
            return None
