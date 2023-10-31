"""Generate a blog post from a text file."""

import os

import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

from src import utils


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

    def _format_to_markdown(self, text):
        lines = text.split("\\n")

        formatted_lines = []

        for line in lines:
            if line.startswith("#"):
                if formatted_lines:
                    formatted_lines.append("")
            formatted_lines.append(line)

        formatted_text = "\n".join(formatted_lines)

        return formatted_text

    def generate_blog(self, text_file_path):
        """Generate a blog post from a text file.

        Args:
            text_file_path (str): The path to the text file.

        Returns:
            str: The path to the generated blog post.

        Raises:
            ValueError: If the total token count exceeds 4000.
        """
        input_text = self._read_text_file(text_file_path)
        system_message_content = "You're a tech blog writer. And write blog entries using markedown, like header and lists."
        token_count = self._count_tokens(system_message_content) + self._count_tokens(
            input_text,
        )

        if token_count > 4000:
            raise ValueError(
                "The total token count exceeds 4000, please reduce the text length.",
            )

        messages = [
            SystemMessage(content=system_message_content),
            HumanMessage(content=input_text),
        ]

        result = self.chat.invoke(messages)
        output_file_name = os.path.basename(text_file_path).replace(".txt", ".md")
        output_path = self._save_to_file(result.content, output_file_name)
        return output_path

    def _save_to_file(self, content, output_file_name):
        output_path = os.path.join(self.output_path, output_file_name)
        with open(output_path, "w") as f:
            f.write(content)
        utils.logging.info(f"Blog post saved to: {output_path}")
        return output_path
