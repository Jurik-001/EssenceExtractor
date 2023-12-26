from essence_extractor import YouTubeDownloader
import os


def test_short_url(tmp_path):
    url = "https://youtu.be/9bZkp7q19f0"
    output_path = tmp_path / "videos"

    downloader = YouTubeDownloader(output_path=str(output_path))
    video_path = downloader.download_video(url)

    assert video_path is not None
    assert os.path.exists(video_path)
