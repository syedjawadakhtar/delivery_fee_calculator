# Delivery Fee Calculator [Backend]

By [Syed Jawad Akhtar](https://github.com/syedjawadakhtar)

This is an HTTP API which could be used for calculating delivery fees when a customer is ready with their shopping cart. It is written in Python using the Flask framework. The API is documented using Swagger Editor in swagger.yml. The delivery price depends on the cart value, the number of items in the cart, the time of the order, and the delivery distance.

## Table of Content

1. [Codebase Tree](#codebase-tree)
2. [Specifications of the task](#specifications-of-the-task)
3. [Setup](#setup)
4. [Running the app](#running-the-app)
5. [Tests](#tests)

## Codebase Tree

```bash
.
├── README.md              # This file
├── requirements.txt       # Requirements to run the app
├── swagger.yml            # Swagger doceumentation
├── src
  ├── app.py                 # Main application
  └── main.py                # delivery calculator logic
└── tests
  ├── test_api.py            # tests the API
  └── test_main.py           # tests for delivery calculator logic
```

## Specifications of the task

Rules for calculating a delivery fee:

- If the cart value is less than 10€, a small order surcharge is added to the delivery price. The surcharge is the difference between the cart value and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€.
- A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.
  - Example 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
  - Example 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
  - Example 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€
- If the number of items is five or more, an additional 50 cent surcharge is added for each item above and including the fifth item. An extra "bulk" fee applies for more than 12 items of 1,20€
  - Example 1: If the number of items is 4, no extra surcharge
  - Example 2: If the number of items is 5, 50 cents surcharge is added
  - Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
  - Example 4: If the number of items is 13, 5,70€ surcharge is added ((9 * 50 cents) + 1,20€)
  - Example 5: If the number of items is 14, 6,20€ surcharge is added ((10 * 50 cents) + 1,20€)
- The delivery fee can never be more than 15€, including possible surcharges.
- The delivery is free (0€) when the cart value is equal or more than 200€.
- During the Friday rush, 3 - 7 PM, the delivery fee (the total fee including possible surcharges) will be multiplied by 1.2x. However, the fee still cannot be more than the max (15€). Considering timezone, for simplicity, use UTC as a timezone in backend solutions (so Friday rush is 3 - 7 PM UTC). In frontend solutions, use the timezone of the browser (so Friday rush is 3 - 7 PM in the timezone of the browser).

## Setup

To install all the dependencies of my project, please run the command below in the project directory:
```pip install -r requirements.txt```

## Running the app

Run the application directly from Flask

```bash
FLASK_APP=src/app.py flask run
```

To send data using the terminal:

1. Bash:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T16:00:00Z"}' http://127.0.0.1:5000/cart
```

2. PowerShell:

```ps
Invoke-RestMethod -Uri http://127.0.0.1:5000/cart -Method Post -Body '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}' -Headers @{"Content-Type"="application/json"}
```

3. Command Prompt:

```cmd
curl -X POST -H "Content-Type: application/json" -d "{\"cart_value\": 790, \"delivery_distance\": 2235, \"number_of_items\": 4, \"time\": \"2024-01-15T16:00:00Z\"}" http://127.0.0.1:5000/cart
```

Or you can use [Postman](https://www.postman.com/) for a nice UI to enter the data.

API documentation is on Swagger. It can viewed on the browser on the URL after running the app: [http://localhost:5000/api/docs/](http://localhost:5000/api/docs/)

## Tests

There 2 testing scripts in the project `test_main.py` and `test_api.py` totally to 12 tests.

To run tests make sure you have installed pytest.

Then run `pytest` to get test results of both the scripts.

- Testing the delivery logic with the given specifications:

There are 7 unit tests in `test_main.py`. It checks the delivery fee outputs for inputs such as:

1. Normal cart value
2. High cart value
3. Bulk items
4. Rush hour on friday
5. Not rush hour on Friday
6. Not a Friday
7. Invalid time format %Y-%m-%dT%H:%M:%SZ

- Testing the API:

There are 4 unit tests in `test_api.py`. It checks for API response codes and error statements. It tests if:

1. Requested data is valid.
2. There are any missing data from the request payload.
3. There any fields that are of incorrect datatypes.
4. Time parameter is not in the correct format.
5. Time parameter is in future.