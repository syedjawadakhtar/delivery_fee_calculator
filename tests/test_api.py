### Unit tests for testing the API with it's response codes and error statements. ### 


import pytest
from src.app import app

@pytest.fixture
def client():
    """
    Setting up Flask test client
    """
    with app.test_client() as client:
        yield client

@pytest.fixture
def valid_request():
    """
    Valid payload request
    """
    return {
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z"
    }

@pytest.fixture
def invalid_request_missing_field():
    """
    Missing parameter in payload request
    """
    return {
        "cart_value": 790,
        "delivery_distance": 2235,
        # Missing 'number_of_items' field
        "time": "2024-01-15T13:00:00Z"
    }

@pytest.fixture
def invalid_request_incorrect_datatype():
    """
    cart_value is string which is should be integer
    """
    return {
        "cart_value": "790",
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z"
    }

@pytest.fixture
def invalid_request_incorrect_time():
    """
    Time is not in correct format
    """
    return {
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "15 January 2024 3 hrs 25 minutes 25 seconds"
    }

@pytest.fixture
def invalid_request_future_time():
    """
    Time is in future
    """
    return {
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2025-01-15T13:00:00Z"
    }

def test_valid_request(client, valid_request):
    """ 
    Tests if the requested data is valid.
    """
    response = client.post('/cart', json=valid_request)
    assert response.status_code == 200
    data = response.get_json()
    assert "delivery_fee" in data

def test_invalid_request_missing_field(client, invalid_request_missing_field):
    """
    Tests if there are any missing data from the request payload
    """
    response = client.post('/cart', json=invalid_request_missing_field)
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data
    assert "Missing required field: number_of_items" in data["error"]

def test_invalid_request_incorrect_datatype(client, invalid_request_incorrect_datatype):
    """
    Tests if there any fields that are of incorrect datatype
    """
    response = client.post('/cart', json=invalid_request_incorrect_datatype)
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data
    assert "Invalid field: cart_val" in data["error"]

def test_invalid_request_incorrect_time(client, invalid_request_incorrect_time):
    """
    Tests if time parameter is not in the correct format
    """
    response = client.post('/cart', json=invalid_request_incorrect_time)
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data
    assert "Time is not in the correct format: 15 January 2024 3 hrs 25 minutes 25 seconds" in data["error"]

def test_invalid_request_future_time(client, invalid_request_future_time):
    """
    Tests if time paramter is in future
    """
    response = client.post('/cart', json=invalid_request_future_time)
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data
    assert "Time is in future, this is impossible unless you're a time traveler." in data["error"]

