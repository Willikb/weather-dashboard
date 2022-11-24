from flask import Flask, render_template, request
import configparser
import requests
from datetime import datetime
from datetime import timezone


app = Flask(__name__)
app.debug = True


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    temp_units = request.form['temp_units']
    api_key = get_api_key()
    if temp_units == 'F':
        data = get_weather_results_imperial(zip_code, api_key)
        temp = data["main"]["feels_like"]
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    else:
        data = get_weather_results_metric(zip_code, api_key)
        temp = data["main"]["feels_like"]
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])

    data = get_weather_results(zip_code, api_key)
    icon = data["weather"][0]["icon"]
    icon_url = "https://openweathermap.org/img/w/" + icon + ".png"
    weather = data["weather"][0]["main"]
    location = data["name"]
    sunrise = data["sys"]["sunrise"]
    dt_obj = datetime.fromtimestamp(int(sunrise))
    dt = str(datetime.now(timezone.utc))[0:19]
    now = str(datetime.now())[0:19]
    return render_template('results.html',
                           location=location, temp=temp,
                           feels_like=feels_like, weather=weather , icon_url=icon_url, sunrise=sunrise,
                           dt_obj=dt_obj, dt=dt, now=now)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_results(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

print(get_weather_results_metric("95129", get_api_key()))
