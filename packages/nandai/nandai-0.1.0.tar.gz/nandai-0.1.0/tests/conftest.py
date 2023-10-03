import pytest
from pytest_mock import MockFixture
from unittest.mock import AsyncMock


@pytest.fixture
def mock_http_post(mocker: MockFixture) -> AsyncMock:
    json_mock = mocker.MagicMock()
    json_mock.json = mocker.MagicMock()
    mock = AsyncMock()
    mock.return_value = json_mock
    mocker.patch('nandai.api.http_client.post', mock)
    return json_mock.json
