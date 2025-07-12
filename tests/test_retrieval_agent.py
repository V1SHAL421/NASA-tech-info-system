import pytest
import requests
import logging

from agents.retrieval_agent import query_nasa_api

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = True
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

@pytest.fixture
def mock_response():
    yield {
        "status_code": 200,
        "response": {"data": []}
    }

# @pytest.mark.unit
# def test_query_nasa_api(mocker):
#     mock_api_call = mocker.patch(requests.get, return_value=mock_response)
#     assert query_nasa_api("test_query") == {"data": []}

@pytest.mark.integration
def test_query_nasa_api_integration():
    response = query_nasa_api.invoke("I want to know more about Mars tech projects")
    logger.info(f"Response: {response}")
    assert isinstance(response, dict)
    assert "error" not in response