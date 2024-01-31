### Unit tests for testing the application specifications of the assignment ### 

from src.main import delivery_fee_calculator, time_cal

def test_delivery_fee_calculator_normal():
    """
    Tests the value of the delivery fees when cart value is normal. 
    """
    result = delivery_fee_calculator(790, 2235, 4, "2024-01-15T13:00:00Z")
    assert result == 710

def test_delivery_fee_calculator_high_cart_value():
    """
    Tests the value of the delivery fees when cart value is high.
    """
    result = delivery_fee_calculator(25000, 2235, 4, "2024-01-15T13:00:00Z")
    assert result == 0

def test_delivery_fee_calculator_bulk_items():
    """
    Tests the value of the delivery fees when the numner of items are high
    """
    result = delivery_fee_calculator(1500, 2235, 15, "2024-01-15T13:00:00Z")
    assert result == 1170

def test_time_cal_rush_hour_friday():
    """
    Tests the value of the delivery fees when time is in rush hours on Friday 19th Jan
    """
    result = time_cal("2024-01-19T16:30:00Z")
    assert result == 1.5

def test_time_cal_not_rush_hour_friday():
    """
    Tests the value of the delivery fees when it's on Friday but not rush hours
    """
    result = time_cal("2024-01-19T13:30:00Z")
    assert result == 1

def test_time_cal_not_friday():
    """
    Tests the value of the delivery fees when the day is not a Friday
    """
    result = time_cal("2024-01-15T13:30:00Z")
    assert result == 1

def test_time_cal_invalid_format():
    """
    Tests the value of the delivery fees when the time formay is not of the form '%Y-%m-%dT%H:%M:%SZ'
    """
    try:
        time_cal("2024-01-15T16:30:00")
    except ValueError as e:
        assert str(e) == "time data '2024-01-15T16:30:00' does not match format '%Y-%m-%dT%H:%M:%SZ'"
