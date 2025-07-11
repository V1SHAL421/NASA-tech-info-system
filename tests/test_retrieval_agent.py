import pytest
import requests

from agents.retrieval_agent import query_nasa_api

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
    response = query_nasa_api.invoke("engine")
    assert isinstance(response, dict)
    assert "error" not in response