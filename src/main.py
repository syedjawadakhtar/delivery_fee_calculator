"""
Main function containing the logic for calculation of delivery fees. 
Following the rules for calculating delivery fees.

Taking these following data as input (JSON)
Total cart value (cents) - cart_value
Total distance(meters) - delivery_distance
Number of items (number) - number_of_items
Delivery time (UTC)- delivery_time
"""

import math
from datetime import datetime

def less_cart(cart_val):
    """Calculate surcharge when cart value is less than 10€."""
    if cart_val < 1000:
        return  (1000 - cart_val)
    else:
        return 0


def distance_cal(delivery_distance):
    """Calculate delivery fees based on distance. Base fee + additional fees on every 500 meters"""
    base_fee = 200
    # Removing the initial 1 km from the distance
    distance = delivery_distance - 1000
    if distance < 0: return base_fee
    else:    
        # Returning base fee + Ceiling value of the distance
        return base_fee + (math.ceil(distance/500)*100)


def items_cal(items):
    """Calculate surcharge based on the number of items. Extra charge on bulk items (>12)."""
    surcharge = 0
    if (items>=5):
        surcharge = (items-4)*50
    # Add Bulk charge
    if (items>12):
        surcharge += 120
    return surcharge


def time_cal(time):
    """Calculate rush hour charges multiplier."""
    delivery_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    start_time = datetime.strptime("15:00:00", "%H:%M:%S").time()
    end_time = datetime.strptime("19:00:00", "%H:%M:%S").time()

    if delivery_time.weekday() == 4:
        if start_time <= delivery_time.time() <= end_time:
            return 1.5  # Multiply delivery fees by 1.5 during rush hour
    return 1

def delivery_fee_calculator(cart_val, delivery_distance, number_of_items, time):
    """Calculate effective delivery fees"""
    if cart_val >= 20000:
        return 0
    else:    
        delivery_fees = less_cart(cart_val) + distance_cal(delivery_distance) + items_cal(number_of_items)
        delivery_fees *=  time_cal(time)
        delivery_fees = max(delivery_fees, 15)
    
    return int(delivery_fees)
