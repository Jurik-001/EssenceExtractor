from unittest.mock import patch
from src import CostManager
from src import utils


def test_calculate_cost_token():
    cost_manager = CostManager(utils.DEFAULT_MODEL_NAME)
    input_cost = cost_manager.calculate_cost_token(500, is_input=True)
    output_cost = cost_manager.calculate_cost_token(500, is_input=False)
    assert input_cost == 500 / 1000 * cost_manager.input_token_cost
    assert output_cost == 500 / 1000 * cost_manager.output_token_cost


@patch('src.utils.TokenCounter.count_tokens')
def test_calculate_cost_text(mock_count_tokens):
    mock_count_tokens.return_value = 500
    cost_manager = CostManager(utils.DEFAULT_MODEL_NAME)
    cost = cost_manager.calculate_cost_text("some text", is_input=True)
    assert cost == 500 / 1000 * cost_manager.input_token_cost


def test_get_total_cost():
    cost_manager = CostManager(utils.DEFAULT_MODEL_NAME)
    cost_manager.calculate_cost_token(500, is_input=True)
    cost_manager.calculate_cost_token(300, is_input=False)
    total_cost = cost_manager.get_total_cost()
    expected_cost = (500 / 1000 * cost_manager.input_token_cost) + \
                    (300 / 1000 * cost_manager.output_token_cost)
    assert total_cost == expected_cost


