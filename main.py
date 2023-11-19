"""Generate a blog post from a YouTube video."""

import argparse
import os

from src import utils
from src.blog_generator import BlogGenerator
from src.downloader import YouTubeDownloader
from src.transcriber import Transcriber
from src.image_extractor import BlogMediaEnhancer


def main(output_dir, api_key):
    """Download, transcribe, and generate blog post of a YouTube video.

    Args:
        output_dir (str): The directory to save the summary file.
        api_key (str): The API key for openai API.
    """
    os.environ["OPENAI_API_KEY"] = api_key
    yt_downloader = YouTubeDownloader(output_path=output_dir)
    transcriber = Transcriber(output_path=output_dir)
    blog_generator = BlogGenerator(output_path=output_dir)
    image_path = os.path.join(output_dir, "images")
    image_extractor = BlogMediaEnhancer(output_path=image_path)

    url = input("Please enter the YouTube video URL: ")

    video_path = yt_downloader.download_video(url)
    utils.logging.info(f"Video downloaded to: {video_path}")

    audio_path = transcriber.extract_audio(video_path)
    utils.logging.info(f"Audio extracted to: {audio_path}")

    transcription_path = transcriber.transcribe_audio(audio_path)
    utils.logging.info(f"Audio transcribed to: {transcription_path}")

    blog_content = blog_generator.generate_blog(transcription_path)
    utils.logging.info(f"Blog post generated")

    blog_content = image_extractor.add_images_to_blog(video_path, blog_content)
    utils.logging.info(f"Images added to blog post")

    blog_content = utils.format_to_markdown(blog_content)

    blog_post_name = video_path.replace(".mp4", "")

    blog_post_path = os.path.join(
        output_dir, f"{os.path.basename(blog_post_name)}.md",
    )
    utils.save_to_md_file(blog_content, blog_post_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download, transcribe, and summarize a YouTube video.",
    )
    parser.add_argument(
        "output_dir", type=str, help="The directory to save the summary file.",
    )
    parser.add_argument("api_key", type=str, help="The API key for openai API.")
    args = parser.parse_args()
    main(args.output_dir, args.api_key)
