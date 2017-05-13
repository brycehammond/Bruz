import requests
import time
from datetime import date
from flask import Flask
from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

@ask.launch
def hello():

    welcome_msg = "Welcome to Bruz Beers."

    return statement(welcome_msg)


@ask.intent("FoodTruckIntent", convert={'date': 'date'}, default={'date': date.today()})
def food_truck(date):

    truck_msg = "The food truck is Mile High Burgers on {0:%B} {0:%d}".format(date)

    return statement(truck_msg)


if __name__ == '__main__':

    app.run(debug=True)