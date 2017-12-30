import requests
import time
from datetime import date
from flask import Flask
from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

@ask.launch
def hello():

    welcome_msg = "Welcome to Bruz Beers. You can ask Bruz what food truck is there today or on a given date. Would you like to know what food truck is there today?"

    return question(welcome_msg)


@ask.intent("FoodTruckIntent", convert={'date': 'date'}, default={'date': date.today()})
def food_truck(date):

    request = requests.get("http://bruz.improbabilitydrive.com/foodtrucks.json")
    trucks_json = request.json()
    search_date = date.strftime("%Y-%m-%d")

    if request.status_code == 200:
        truck_json = filter(lambda x: x['date'] == search_date, trucks_json)
        if len(truck_json) > 0:
            truck_json = truck_json[0] #set to first element
            if date == date.today():
                when_there = "today"
            else:
                when_there = "on {0:%A} {0:%B} {0.day}{1}".format(date, _day_suffix(date.day))

            speech = "{0} is at Bruz from {1} to {2} {3}".format(truck_json['name'], truck_json['start_time'], truck_json['end_time'], when_there)
        else:
            speech = "So sorry, There is no food truck at Bruz on {0:%B} {0:%d}".format(date)

    else:
        speech = "There was a problem finding the food trucks for Bruz Beers"

    return statement(speech)

@ask.intent("YesIntent")
def today_foodtruck():
    return food_truck(date.today())

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... goodbye'
    return statement(bye_text)

@ask.intent('AMAZON.HelpIntent')
def help():
    return statement("You can ask Bruz what food truck is there today or on a given date.")


@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = "Goodbye"
    return statement(bye_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    bye_text = "Goodbye"
    return statement(bye_text)

def _day_suffix(day):
    return 'th' if 11 <= day <= 13 else {1:'st',2:'nd',3:'rd'}.get(day % 10, 'th')

if __name__ == '__main__':

    app.run(debug=True)