import requests
from datetime import datetime
import smtplib
from time import sleep
import email_pass_api_key as ep


# My latitude and longitude
MY_LAT = ep.MY_LAT
MY_LONG = ep.MY_LONG
# My email and password
MY_EMAIL = ep.EMAIL
MY_PASSWORD = ep.PASSWORD


def iss_location():
    # Get data from the api and store that data in response.
    response = requests.get('http://api.open-notify.org/iss-now.json')
    response.raise_for_status()         # Raise error when not able to get data from the url.

    data = response.json()
    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])
    # iss_location = (iss_latitude, iss_longitude)

    # Your position within +5 and -5 degree of the iss position.
    if (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5) and (MY_LONG -5 <= iss_longitude <=MY_LONG + 5):
        return True


def is_night():
    # Sunrise and Sunset api
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 0,
    }
    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
    # sunrise_sunset_time = (sunrise, sunset)

    # Current time
    current_time = datetime.now().hour

    if (current_time <= sunrise) and (current_time >= sunset):
        # it's dark now i.e it's night.
        return True


while True:
    # This is an infinite loop which will run 24 * 7.
    # This will send and email in every 60 second when the ISS is overhead and it's night.
    sleep(60)
    if iss_location() and is_night():
        connection = smtplib.SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=ep.MY_EMAIL,
            msg='Subject: Look UP \n\n\n\nThe ISS is above you in the sky.'
        )