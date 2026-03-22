import pytest
from unittest.mock import MagicMock
from database.schema import Ingest
from services.data_service import DataService  # adjust import

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def service(mock_session):
    return DataService(mock_session)

def test_post_data_success(service, mock_session):
    data = [
        {"base_url": "a.com", "url_ext": "/1"},
        {"base_url": "b.com", "url_ext": "/2"},
    ]

    result = service.post_data(data)

    # Check objects were created
    assert mock_session.add_all.called

    # Extract passed objects
    args, _ = mock_session.add_all.call_args
    ingest_objects = args[0]

    assert len(ingest_objects) == len(data)
    assert all(isinstance(object, Ingest) for object in ingest_objects)

    mock_session.commit.assert_called_once()
    assert result == data

def test_post_data_failure(service, mock_session):
    data = [{"base_url": "a.com", "url_ext": "/1"}]

    mock_session.commit.side_effect = Exception("DB error")

    result = service.post_data(data)

    assert result is None

def test_get_sources(service, mock_session):
    expected = [("a.com", "/1"), ("b.com", "/2")]

    query_mock = mock_session.query.return_value
    distinct_mock = query_mock.distinct.return_value
    distinct_mock.all.return_value = expected

    result = service.get_sources()

    mock_session.query.assert_called_once_with(
        Ingest.base_url, Ingest.url_ext
    )
    query_mock.distinct.assert_called_once()
    distinct_mock.all.assert_called_once()

    assert result == expected