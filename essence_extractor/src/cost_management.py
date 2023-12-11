"""This module is used to calculate the cost of a text."""

from essence_extractor.src import utils


class CostManager:
    """This class is used to calculate the cost of a text.

    Attributes:
        model_name (str): The name of the model to use.
    """
    def __init__(self, model_name):
        self.model_name = model_name
        self.input_token_cost = \
            utils.MODEL_TOKEN_LENGTH_MAPPING[model_name]["input_token_cost"]
        self.output_token_cost = \
            utils.MODEL_TOKEN_LENGTH_MAPPING[model_name]["output_token_cost"]
        self.token_counter = utils.TokenCounter(self.model_name)
        self.total_cost = 0
        self.per_n_tokens = 1000

    def calculate_cost_token(self, token_count, is_input=True):
        """Calculate the cost of a text.

        Args:
            token_count (int): The number of tokens in the text.
            is_input (bool, optional): Whether text is input or output. Defaults to True.

        Returns:
            float: The cost of the text.
        """
        if is_input:
            cost = (token_count / self.per_n_tokens) * self.input_token_cost
        else:
            cost = (token_count / self.per_n_tokens) * self.output_token_cost
        self.total_cost += cost
        return cost

    def calculate_cost_text(self, text, is_input=True):
        """Calculate the cost of a text.

        Args:
            text (str): The text to calculate the cost of.
            is_input (bool, optional): Whether the text is an input or an output.
                Defaults to True.

        Returns:
            float: The cost of the text.
        """
        token_count = self.token_counter.count_tokens(text)
        return self.calculate_cost_token(token_count, is_input=is_input)

    def get_total_cost(self):
        """Get the total cost of the text.

        Returns:
            float: The total cost of the text.
        """
        return self.total_cost