from essence_extractor import YouTubeDownloader
import os


def test_short_url():
    url = "https://youtu.be/9bZkp7q19f0"
    output_path = "videos"
    downloader = YouTubeDownloader(output_path=output_path)
    video_path = downloader.download_video(url)
    assert video_path is not None
    assert os.path.exists(video_path)

    # cleanup
    os.remove(video_path)
    os.rmdir(output_path)
