"""Adds images to a blog post based on the content of the blog post."""

import math
import os
import re

import faiss
import numpy as np
import pytesseract
from moviepy.editor import VideoFileClip
from sentence_transformers import SentenceTransformer

from essence_extractor.src import utils
from essence_extractor.src.data_models import YouTubeURL


class BlogMediaEnhancer:
    """Adds images to a blog post based on the content of the blog post.

    Attributes:
        output_path (str): The path to the output directory.
    """
    def __init__(self, output_path='images'):
        self.output_path = output_path
        self.image_dir_name = 'images'
        self.image_output_path = os.path.join(output_path, self.image_dir_name)
        self.model = SentenceTransformer(
            'sentence-transformers/paraphrase-multilingual-mpnet-base-v2',
        )
        if not os.path.exists(self.image_output_path):
            os.makedirs(self.image_output_path)

    def _extract_images(self, video_file_path, interval=10):
        """Extracts images from the video at the specified interval.

        Args:
            video_file_path (str): The path to the video file.
            interval (int): The interval at which to extract images, in seconds.

        Returns:
            List[str]: A list of paths to the extracted images.
        """
        if not isinstance(interval, int) or interval <= 0:
            raise ValueError("Interval must be a positive integer")

        if not os.path.exists(self.image_output_path):
            os.makedirs(self.image_output_path)

        video = VideoFileClip(video_file_path)
        duration = video.duration

        if interval > duration:
            raise ValueError("Interval cannot be longer than the video duration")

        extracted_images = {}

        for i in range(0, math.ceil(duration), interval):
            frame = video.get_frame(i)
            frame_image_filename = f'frame_at_{i}_seconds.png'
            frame_image_path = os.path.join(self.image_output_path, frame_image_filename)
            video.save_frame(frame_image_path, t=i)
            extracted_images[frame_image_filename] = frame

        video.close()

        return extracted_images

    def _extract_text_from_image(self, img):
        """Extracts text from the given image.

        Args:
            img (PIL.Image): The image to extract text from.

        Returns:
            str: The extracted text.
        """
        try:
            text = pytesseract.image_to_string(img)
        except Exception as e:
            utils.logging.info(f"Error processing {e}")
            text = ""
        return text

    def _embed_text(self, text):
        """Embeds the given texts using the specified SentenceTransformer model.

        Args:
            text (str): The text to embed.

        Returns:
            A list of numpy arrays, each representing the embedded text.
        """
        embeddings = self.model.encode(text, show_progress_bar=False)

        return embeddings

    def _create_index(self, embeddings):
        """Creates an index for the given embeddings.

        Args:
            embeddings (List[np.array]): The embeddings to create the index for.

        Returns:
            A Faiss index.
        """
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index

    def _query_index(self, index, embedded_query, images_text_dict, k=1):
        """Queries the given index with the given query.

        Args:
            index (faiss.Index): The index to query.
            embedded_query (np.array): The query to use.
            images_text_dict (dict): A dict mapping image names to their embedded text.
            k (int): The number of results to return.

        Returns:
            List[str]: A list of image names, representing the retrieved images.
        """
        _, retrieved_idxs = index.search(embedded_query, k=k)
        retrieved_image_names = [
            list(images_text_dict.keys())[idx] for idx in retrieved_idxs[0]
        ]
        return retrieved_image_names

    def _extract_alt_text_with_image_tags(self, markdown_content):
        """Extracts alt text and image markdown tags from markdown content.

        Args:
            markdown_content (str): The markdown content to extract from.

        Returns:
            dict: A dictionary mapping alt text to their respective image markdown tags.
        """
        image_pattern = re.compile(r'(!\[.*?\]\(\s*.*?\s*(?: ".*?")?\s*\))')
        description_image_tags = {}

        lines = markdown_content.split('\n')

        for line in lines:
            image_match = image_pattern.search(line)
            if image_match:
                image_tag = image_match.group(1).strip()
                alt_text_match = re.search(r'!\[(.*?)\]', image_tag)
                if alt_text_match:
                    alt_text = alt_text_match.group(1).strip()
                    description_image_tags[alt_text] = image_tag

        return description_image_tags

    def _remove_unused_images(self, keep_image_names):
        """Removes the images that are not used in the blog post.

        Args:
            keep_image_names (List[str]): A list of image names to keep.
        """
        for img_name in os.listdir(self.image_output_path):
            if img_name not in keep_image_names:
                os.remove(os.path.join(self.image_output_path, img_name))

    def add_images_to_blog(self, video_file_path, blog_content):
        """Adds the images to the blog content.

        Args:
            video_file_path (str): The path to the video file.
            blog_content (str): The blog content.

        Returns:
            str: The blog content with the images added.
        """
        images_dict = self._extract_images(video_file_path)
        image_placeholder_queries = self._extract_alt_text_with_image_tags(blog_content)

        images_text_dict = {}
        for img_name, img in images_dict.items():
            text = self._extract_text_from_image(img)
            embedded_text = self._embed_text(text)
            images_text_dict[img_name] = embedded_text

        embeddings = [embedding for img_name, embedding in images_text_dict.items()]
        embeddings = np.array(embeddings)

        index = self._create_index(embeddings)

        used_images = []

        for alt_text, img_tag in image_placeholder_queries.items():
            query = self._embed_text(alt_text)
            query = query.reshape(1, -1)
            retrieved_image_name = self._query_index(
                index, query, images_text_dict, k=1,
            )[0]
            used_images.append(retrieved_image_name)
            image_path = os.path.join(self.image_dir_name, retrieved_image_name)
            blog_content = blog_content.replace(
                img_tag, f"![{alt_text}]({image_path})",
            )

        self._remove_unused_images(used_images)

        return blog_content

    def add_url_timestamps_to_blog(self, youtube_url, blog_content):
        """Adds url with timestamp to the blog content in Markdown format.

        Args:
            youtube_url (str): The YouTube URL.
            blog_content (str): The blog content.

        Returns:
            str: The blog content with the URL and the
            first timestamp of a range added in Markdown format.
        """
        youtube_url = YouTubeURL(url=youtube_url).url
        timestamp_pattern = r"\[(\d{1,2}):(\d{2}) - \d{1,2}:\d{2}\]"

        def timestamp_to_link(match):
            first_minutes, first_seconds = match.group(1), match.group(2)
            total_seconds = int(first_minutes) * 60 + int(first_seconds)
            full_range = match.group(0)
            return f"{full_range}({youtube_url}&t={total_seconds}s)"

        return re.sub(timestamp_pattern, timestamp_to_link, blog_content)

