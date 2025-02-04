#!/usr/bin/python3
"""HNG Backend Stage 1"""

import requests, math
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

#Disable Python Dictionary Key sorting
app.json.sort_keys = False


def is_prime(number):
    """Checks if a number is prime or not
    
        Args: 'number' which has to be integer

        Returns: Boolean
    """
    if type(number) != int: # if number is an integer
        return False
    
    if number < 2: # if number is less than two
        return False
    
    if number in (2,3): # if number is either 2 or 3
        return True
    
    if number % 2 == 0 or number % 3 == 0: # if number is a multiple of 2 or 3
        return False

    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6

    return True


def is_perfect(number):
    """Checks if a positive integer  equal to the sum of its proper divisors
    
        Args: 'number' which has to be integer

        Returns: Boolean
    """
    divisors = []
    sum = 0
    if type(number) != int: # if number is an integer
        return False
    
    if number < 2: # if number is less than two
        return False
    
    for num in range(1, number):
        if number % num == 0:
            divisors.append(num)

    for n in divisors:
        sum += n

    if sum == number:
        return True
    else:
        return False

def even_or_odd(number):
    """Checks if the given number is even or odd.
    
        Args: 'number' which has to be integer

        Returns: A string that is either even or odd
    """
    value = ""

    if number % 2 == 0:
        value = 'even'
    else:
        value = 'odd'

    return value

def armstrong(number):
    """
        Checks if the given number is equal to the sum of its digits,
        each raised to the power of the number of digits in the number

        Args: 'number' which has to be integer

        Returns: String if armstrong, None if not
    """

    value = ''
    sum = 0

    if number < 1:
        value = None
        return value

    digs = [n for n in str(number)]
    num_digits = len(digs)

    for n in digs:
        sqrd = (int(n) ** num_digits)
        sum += sqrd

    if sum == number:
        value = 'armstrong'
    else:
        value = None

    return value

def properties(number):
    """List the properties of the given number.
    
        Args: 'number' which has to be integer

        Returns: A list of properties e.g Armstrong, Even or Odd 
    """
    properties = []

    value_1 = armstrong(number)
    value_2 = even_or_odd(number)

    properties.append(value_1)
    properties.append(value_2)

    return properties

def digit_sum(number):
    """Calculates the sum of the individual digits that make up the number.
    
        Args: 'number' which has to be integer

        Returns: Sum of type int
    """
    sum = 0
    digs = [n for n in str(number) if n != '-']
    for n in digs:
        sum += int(n)
    return sum
            

@app.route("/api/classify-number")
def display_info():
    """The main API route of this system
    
        Args: 'number' which has to be an integer

        Returns: data on 200 status, error o 400 status
    """

    number_in_tab = request.args.get('number', "")

    try:
        number_in = int(number_in_tab)
    except ValueError:
        error = {
            "number": f'{number_in_tab}',
            "error": True
        }
        return jsonify(error), 400

    u = str(number_in)
    url = 'http://numbersapi.com/'
    url_link = url + u + '/math'
    
    response = requests.get(url_link)

    data = {
        'number': number_in,
        'is_prime': is_prime(number_in),
        'is_perfect': is_perfect(number_in),
        'properties': [v for v in properties(number_in) if v],
        'digit_sum': digit_sum(number_in),
        'fun_fact': response.text
    }

    if response.status_code == 200:
        return jsonify(data)

    elif response.status_code == 400:
        error = {
            "number": "alphabet",
            "error": True
            }
        return jsonify(error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
