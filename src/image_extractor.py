from moviepy.editor import VideoFileClip
import math
import pytesseract
import numpy as np
import os
from sentence_transformers import SentenceTransformer
import faiss
import re
from src import utils


class ImageExtractor:
    def __init__(self, output_path='images'):
        self.output_path = output_path
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def _extract_images(self, video_file_path, interval=10):
        """
        Extracts images from the video at the specified interval.

        Args:
            video_file_path (str): The path to the video file.
            interval (int): The interval at which to extract images, in seconds.

        Returns:
            List[str]: A list of paths to the extracted images.
        """
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        video = VideoFileClip(video_file_path)
        duration = video.duration
        extracted_images = {}

        for i in range(0, math.ceil(duration), interval):
            frame = video.get_frame(i)
            frame_image_filename = f'frame_at_{i}_seconds.png'
            frame_image_path = os.path.join(self.output_path, frame_image_filename)
            video.save_frame(frame_image_path, t=i)
            extracted_images[frame_image_filename] = frame

        video.close()

        return extracted_images

    def _extract_text_from_image(self, img):
        try:
            text = pytesseract.image_to_string(img)
        except Exception as e:
            utils.logging.info(f"Error processing {e}")
            text = ""
        return text

    def _embed_text(self, text):
        """
        Embeds the given texts using the specified SentenceTransformer model.

        Parameters:
        - text str: The text to embed.

        Returns:
        A list of numpy arrays, each representing the embedded text.
        """
        embeddings = self.model.encode(text, show_progress_bar=True)

        return embeddings

    def _create_index(self, embeddings):
        """
        Creates an index for the given embeddings.

        Parameters:
        - embeddings numpy.ndarray: The embeddings to index.

        Returns:
        A Faiss index.
        """
        index = faiss.IndexFlatL2(embeddings.shape[1]) #maybe change to IndexFlatL2
        index.add(embeddings)
        return index

    def _query_index(self, index, embedded_query, images_text_dict, k=1):
        _, retrieved_idxs = index.search(embedded_query, k=k)
        retrieved_image_names = [list(images_text_dict.keys())[idx] for idx in retrieved_idxs[0]]
        return retrieved_image_names

    def _extract_headlines_with_images(self, markdown_content):
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
        for img_name in os.listdir(self.output_path):
            if img_name not in keep_image_names:
                os.remove(os.path.join(self.output_path, img_name))

    def add_images_to_blog(self, video_file_path, blog_content):
        """
        Adds the images to the blog content.

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
            embeded_text = self._embed_text(text)
            images_text_dict[img_name] = embeded_text

        embeddings = [embedding for img_name, embedding in images_text_dict.items()]
        embeddings = np.array(embeddings)

        index = self._create_index(embeddings)

        used_images = []

        for headline, img_tag in image_placeholder_queries.items():
            query = self._embed_text(headline)
            query = query.reshape(1, -1)
            retrieved_image_name = self._query_index(index, query, images_text_dict, k=1)[0]
            used_images.append(retrieved_image_name)
            image_path = os.path.join(self.output_path, retrieved_image_name)
            blog_content = blog_content.replace(img_tag, f"![{retrieved_image_name}]({image_path})")

        print("=====================================")
        print(used_images)
        print("=====================================")
        self._remove_unused_images(used_images)

        return blog_content
