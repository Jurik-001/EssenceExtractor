"""Generate a blog post from a text file."""

import os

import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

from src import utils

MAX_CONTENT_LENGTH = 4000


class BlogGenerator:
    """Generate a blog post from a text file."""

    def __init__(self, output_path="blogs", model_name="gpt-3.5-turbo"):
        self.output_path = output_path
        self.chat = ChatOpenAI(model_name=model_name)
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

    def _matches_token_size(self, token_count):
        # TODO extract supported token length from
        if token_count > MAX_CONTENT_LENGTH:
            return False
        return True

    def format_to_markdown(self, text):
        # TODO move to utils?
        lines = text.split("\\n")

        formatted_lines = []

        for line in lines:
            if line.startswith("#"):
                if formatted_lines:
                    formatted_lines.append("")
            formatted_lines.append(line)

        formatted_text = "\n".join(formatted_lines)

        return formatted_text

    def _entry_generator(self, messages):
        return self.chat.invoke(messages).content


    def generate_blog(self, text_file_path):
        """Generate a blog post from a text file.

        Args:
            text_file_path (str): The path to the text file.

        Returns:
            str: The path to the generated blog post.

        Raises:
            ValueError: If the total token count exceeds MAX_CONTENT_LENGTH.
        """
        input_text = self._read_text_file(text_file_path)
        system_message_content = "You're a tech blog writer. And write blog entries using markedown and placing images using [image] tag."
        token_count = self._count_tokens(system_message_content) + self._count_tokens(
            input_text,
        )

        blog_post = None

        if self._matches_token_size(token_count):
            messages = [
                SystemMessage(content=system_message_content),
                HumanMessage(content=input_text),
            ]
            blog_post = self._entry_generator(messages)
        else:
            utils.logging.info(f"The total token count exceeds {MAX_CONTENT_LENGTH}, long format support will be used.")
            # TODO split up text and generate segments, rewrite sys message so model is aware it generates only segments



        return blog_post
