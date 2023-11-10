import pytest
from fastapi.testclient import TestClient

from phonebook.main import app

client = TestClient(app)


@pytest.fixture
def test_valid_data():
    return {"phone": "1234567890", "address": "Sample Address"}


@pytest.fixture
def test_empty_data():
    return {"phone": "9999999999"}


@pytest.fixture
def test_invalid_data():
    return {"invalid_field": "value"}


def test_check_data_valid(test_valid_data):
    # Write the data
    write_response = client.post("/write_data", json=test_valid_data)
    assert write_response.status_code == 200

    # Check the data
    response = client.get(f"/check_data?phone={test_valid_data['phone']}")
    assert response.status_code == 200
    assert response.json() == test_valid_data


def test_check_data_not_found(test_empty_data):
    # Check the data with no address
    response = client.get(f"/check_data?phone={test_empty_data['phone']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Data not found"}


def test_write_data_invalid_payload(test_invalid_data):
    # Check writing data with invalid payload
    response = client.post("/write_data", json=test_invalid_data)
    assert response.status_code == 422
