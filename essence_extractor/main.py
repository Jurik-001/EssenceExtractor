"""Generate a blog post from a YouTube video."""

import argparse
import os

from tqdm import tqdm

from essence_extractor.src import utils
from essence_extractor.src.blog_generator import BlogGenerator
from essence_extractor.src.blog_media_enhancer import BlogMediaEnhancer
from essence_extractor.src.cost_management import CostManager
from essence_extractor.src.data_models import YouTubeURL
from essence_extractor.src.downloader import YouTubeDownloader
from essence_extractor.src.transcriber import Transcriber


def args_call():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Download, transcribe, and summarize a YouTube video.",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="The directory to save the summary file.",
    )
    parser.add_argument("api_key",
                        type=str,
                        help="The API key for openai API.",
                        )
    parser.add_argument(
        "--model_name",
        type=str,
        default="gpt-3.5-turbo-1106",
        help="The model name used as blog generator.",
    )
    args = parser.parse_args()
    main(args.output_dir, args.api_key, args.model_name)

def main(output_dir, api_key, model_name):
    """Download, transcribe, and generate blog post of a YouTube video.

    Args:
        output_dir (str): The directory to save the summary file.
        api_key (str): The API key for openai API.
        model_name (str): The model name used as blog generator.
    """
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    cost_manager = CostManager(model_name=model_name)
    yt_downloader = YouTubeDownloader(output_path=output_dir)
    transcriber = Transcriber(output_path=output_dir)
    blog_generator = BlogGenerator(
        output_path=output_dir, model_name=model_name, cost_manager=cost_manager,
    )
    media_enhancer = BlogMediaEnhancer(output_path=output_dir)

    youtube_video_url = input("Please enter the YouTube video URL: ")
    youtube_video_url = YouTubeURL(url=youtube_video_url).url

    tasks = ["Downloading Video", "Extracting Audio",
             "Transcribing Audio", "Generating Blog Post",
             "Adding Image Placeholders", "Adding URL Timestamps",
             "Adding Images", "Formatting to Markdown",
             "Saving to File"]

    with tqdm(total=len(tasks)) as pbar:
        video_path = yt_downloader.download_video(youtube_video_url)
        utils.logging.info(f"Video downloaded to: {video_path}")
        pbar.update(1)

        audio_path = transcriber.extract_audio(video_path)
        utils.logging.info(f"Audio extracted to: {audio_path}")
        pbar.update(1)

        transcription_path = transcriber.transcribe_audio(audio_path)
        utils.logging.info(f"Audio transcribed to: {transcription_path}")
        pbar.update(1)

        blog_content = blog_generator.generate_article_content(transcription_path)
        utils.logging.info(f"Blog post generated")
        pbar.update(1)

        blog_content = blog_generator.add_image_placeholder(blog_content)
        utils.logging.info(f"Image placeholders added to blog post")
        pbar.update(1)

        blog_content = media_enhancer.add_url_timestamps_to_blog(
            youtube_video_url, blog_content,
        )
        utils.logging.info(f"URL timestamps added to blog post")
        pbar.update(1)

        blog_content = media_enhancer.add_images_to_blog(video_path, blog_content)
        utils.logging.info(f"Images added to blog post")
        pbar.update(1)

        blog_content = utils.format_to_markdown(blog_content)
        pbar.update(1)

        blog_post_name = video_path.replace(".mp4", "")

        blog_post_path = os.path.join(
            output_dir, f"{os.path.basename(blog_post_name)}.md",
        )
        utils.save_to_md_file(blog_content, blog_post_path)
        pbar.update(1)

    utils.logging.info(f"Blog post cost: {cost_manager.get_total_cost()}$")


if __name__ == "__main__":
    args_call()
