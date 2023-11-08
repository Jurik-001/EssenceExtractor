"""Adds images to a blog post based on the content of the blog post."""

import math
import os
import re

import faiss
import numpy as np
import pytesseract
from moviepy.editor import VideoFileClip
from sentence_transformers import SentenceTransformer

from src import utils


class BlogMediaEnhancer:
    """Adds images to a blog post based on the content of the blog post."""
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
        if not os.path.exists(self.image_output_path):
            os.makedirs(self.image_output_path)

        video = VideoFileClip(video_file_path)
        duration = video.duration
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
        embeddings = self.model.encode(text, show_progress_bar=True)

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

    def _extract_headlines_with_images(self, markdown_content):
        """Extracts the headlines with images from the given markdown content.

        Args:
            markdown_content (str): The markdown content to extract the headlines from.

        Returns:
            dict: A dictionary mapping headlines to their image tags.
        """
        image_pattern = re.compile(r'!\[.*?\]\(\s*(.*?)\s*(?: ".*?")?\s*\)')
        headline_pattern = re.compile(r'^\s*(#{1,6})\s*(.*)', re.MULTILINE)

        headlines_images = {}
        current_headline = None
        lines = markdown_content.split('\n')

        for line in lines:
            headline_match = headline_pattern.match(line)
            if headline_match:
                current_headline = headline_match.group(2).strip()
                continue

            image_match = image_pattern.search(line)
            if image_match and current_headline:
                headlines_images[current_headline] = image_match.string
                current_headline = None

        return headlines_images

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
        image_placeholder_queries = self._extract_headlines_with_images(blog_content)

        images_text_dict = {}
        for img_name, img in images_dict.items():
            text = self._extract_text_from_image(img)
            embedded_text = self._embed_text(text)
            images_text_dict[img_name] = embedded_text

        embeddings = [embedding for img_name, embedding in images_text_dict.items()]
        embeddings = np.array(embeddings)

        index = self._create_index(embeddings)

        used_images = []

        for headline, img_tag in image_placeholder_queries.items():
            query = self._embed_text(headline)
            query = query.reshape(1, -1)
            retrieved_image_name = self._query_index(
                index, query, images_text_dict, k=1,
            )[0]
            used_images.append(retrieved_image_name)
            image_path = os.path.join(self.image_dir_name, retrieved_image_name)
            blog_content = blog_content.replace(
                img_tag, f"![{retrieved_image_name}]({image_path})",
            )

        self._remove_unused_images(used_images)

        return blog_content