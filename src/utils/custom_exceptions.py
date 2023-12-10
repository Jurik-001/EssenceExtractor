"""Custom exceptions for the YouTube Downloader."""

class YouTubeDownloadError(Exception):
    """Exception raised when a YouTube video download fails."""

    def __init__(self, message="Failed to download YouTube video"):
        self.message = message
        super().__init__(self.message)
