"""Generate a blog post from a text file."""

import os

import tiktoken
from openai import OpenAI

from src import utils

MODEL_TOKEN_LENGTH_MAPPING = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-1106": 16385,
    "gpt-4-1106-preview": 128000,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
}
TOKEN_LENGTH_BUFFER = 150
OUTPUT_TOKEN_LENGTH_BUFFER = 1500


class BlogGenerator:
    """Generate a blog post from a text file."""

    def __init__(self, output_path="blogs", model_name="gpt-3.5-turbo"):
        self.model_name = model_name
        self.output_path = output_path
        self.client = OpenAI()
        self.encoding = tiktoken.encoding_for_model(model_name)
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def _read_text_file(self, file_path):
        with open(file_path, "r") as f:
            text = f.read()
        return text

    def _count_tokens(self, text):
        token_count = len(self.encoding.encode(text))
        return token_count

    def format_to_markdown(self, text):
        lines = text.split("\\n")

        formatted_lines = []

        for line in lines:
            if line.startswith("#"):
                if formatted_lines:
                    formatted_lines.append("")
            formatted_lines.append(line)

        formatted_text = "\n".join(formatted_lines)

        return formatted_text

    def _generate_answer(self, system_prompt, user_prompt):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content

    def split_into_first_chunk(self, text, chunk_size, separator=" "):
        words = text.split(separator)
        current_chunk = []
        current_count = 0

        for word in words:
            current_chunk.append(word)
            current_count = self._count_tokens(separator.join(current_chunk))

            if current_count >= chunk_size:
                return separator.join(current_chunk)

        return separator.join(current_chunk)

    def create_refine_prompt(self, existing_answer, text):
        return (
            f"We have provided an existing blog article up to a certain point: {existing_answer}\n"
            "We have the opportunity to refine the existing blog article"
            "(only if needed) with some more context below.\n"
            "------------\n"
            f"{text}\n"
            "------------\n"
            "Given the new context, refine the original blog article"
            "If the context isn't useful, return the original blog article."
        )

    def generate_blog(self, text_file_path):
        """Generate a blog post from a text file.

        Args:
            text_file_path (str): The path to the text file.

        Returns:
            str: The path to the generated blog post.
        """
        input_text = self._read_text_file(text_file_path)
        system_message = "Your role is creating one final version of a ready to publish article based on transcript. Write the article with a focus on educating the reader and a captivating introduction, body, and a concise conclusion, use markdown and placing images using [image] tag.\n"
        system_msg_length = self._count_tokens(system_message)

        user_msg_length = self._count_tokens(self.create_refine_prompt("", ""))
        chunk_size = MODEL_TOKEN_LENGTH_MAPPING[
                         self.model_name] - system_msg_length - user_msg_length - OUTPUT_TOKEN_LENGTH_BUFFER

        blog_post = ""
        while input_text:
            utils.logging.info(f"Chunk size: {chunk_size}")
            chunk = self.split_into_first_chunk(input_text, chunk_size)
            user_message = self.create_refine_prompt(blog_post, chunk)

            blog_post = self._generate_answer(system_message, user_message)
            utils.logging.info(f"Blog post: {blog_post}")
            blog_post_length = self._count_tokens(blog_post)
            utils.logging.info(f"Blog post token count: {blog_post_length}")

            chunk_size = MODEL_TOKEN_LENGTH_MAPPING[
                             self.model_name] - system_msg_length - user_msg_length - blog_post_length - OUTPUT_TOKEN_LENGTH_BUFFER
            input_text = input_text.replace(chunk, "")
            utils.logging.info(f"Remaining token count: {self._count_tokens(input_text)}")

        return blog_post
