"""
Single endpoint /cart [POST], which calculates the delivery fees based on the information in the request payload (JSON) and
includes the calculated delivery fee in the response payload(JSON).

Swagger Documentation included.

"""

import os
from flask import Flask, jsonify, request, send_from_directory
from src.main import delivery_fee_calculator
from datetime import datetime, timezone
from dateutil.parser import isoparse
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger UI route
SWAGGER_URL = '/api/docs'
API_URL = '/docs/swagger.yml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Delivery Calculator API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Swagger documentation route
@app.route('/docs/swagger.yml')
def specs():
    return send_from_directory(os.getcwd(), "swagger.yml")


# Cart endpoint
@app.route('/cart', methods=['POST'])

def cart_api():
    try:
        # Recieve the JSON request payload
        data = request.get_json()

        # Check if the request body is valid
        if not data:
            return jsonify({'error': 'Invalid request body'}), 400

        # Validate input data; missing fields, and if integers
        required_fields = ['cart_value', 'delivery_distance', 'number_of_items']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 422
            if not isinstance(data[field], int) or data[field] <= 0:
                return jsonify({"error": f"Invalid field: {field}"}), 422
        
        # Check if time parameter is present
        if 'time' not in data:
            return jsonify({"error": f"Missing required field: time"}), 422

        # Check if the time paramter string is correctly formatted in ISO 8601
        try:
            if not isinstance(data['time'], str):
                raise ValueError
            
            # Parse the time into UTC format
            data_time = isoparse(data['time']).replace(tzinfo=timezone.utc)

            # Check if the time is in the past instead of future
            try:
                if data_time  > datetime.now(timezone.utc):
                    raise ValueError
            except ValueError:
                return jsonify({'error': "Time is in future, this is impossible unless you're a time traveler."}), 422
                
        except ValueError:
            return jsonify({'error': f"Time is not in the correct format: {data['time']}"}), 422
        
        cart_value = data.get('cart_value', 0)
        delivery_distance = data.get('delivery_distance', 0)
        number_of_items = data.get('number_of_items', 0)
        delivery_time = data.get('time', '2000-00-00T00:00:00Z')
        delivery_fee = delivery_fee_calculator(cart_value, delivery_distance, number_of_items, delivery_time)

        # Response payload
        response = {"delivery_fee":delivery_fee}
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
