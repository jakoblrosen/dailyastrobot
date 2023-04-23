import os
import time
import requests
import random
import schedule
import couchdb
import tweepy

from pathlib import Path
from dotenv import load_dotenv


def get_galaxy():
    dotenv_path = Path('db.env')
    load_dotenv(dotenv_path=dotenv_path)

    COUCH_USER = os.getenv('COUCH_USER')
    COUCH_PASSWORD = os.getenv('COUCH_PASSWORD')
    COUCH_HOST = os.getenv('COUCH_HOST')
    COUCH_PORT = os.getenv('COUCH_PORT')
    couch = couchdb.Server(f'http://{COUCH_USER}:{COUCH_PASSWORD}@{COUCH_HOST}:{COUCH_PORT}')
    db = couch['dailyastrobotdb']
    galaxy_ids = [id for id in db]
    galaxy_id = random.choice(galaxy_ids)
    galaxy = dict(db[galaxy_id].items())
    del db[galaxy_id]
    return galaxy


# calculate time in years given distance in Mly and speed in km/h
def calculate_time(distance, speed):
    KM_TO_MLY = 1.0577e-19
    H_TO_Y = 1.1415e-4
    delta = distance / (speed * (KM_TO_MLY / H_TO_Y))
    return int(delta)


def job():
    dotenv_path = Path('secrets.env')
    load_dotenv(dotenv_path=dotenv_path)

    API_KEY = os.getenv('API_KEY')
    API_KEY_SECRET = os.getenv('API_KEY_SECRET')
    BEARER_TOKEN = os.getenv('BEARER_TOKEN')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    CURRENT_SPACE_TRAVEL_SPEED = 6.92e5     # stored as km/h

    try:
        galaxy = get_galaxy()
        galaxy_name = galaxy.get('name')
        galaxy_code = galaxy.get('code')
        distance = galaxy.get('distance')
        image_url = galaxy.get('image_url')
        fname = f'media/{image_url.split("/")[-1]}'
        photo = requests.get(image_url)
        open(fname, 'wb').write(photo.content)

        NEWLINE = '\n'
        time_to_reach = calculate_time(distance, CURRENT_SPACE_TRAVEL_SPEED)
        message = f'{galaxy_name} ({galaxy_code}){NEWLINE}' \
                  f'Distance: {distance} megalight-years{NEWLINE}' \
                  f'{time_to_reach} years to reach at our current space travel speed'

        media = api.simple_upload(fname)
        api.update_status(status=message, media_ids=[media.media_id])
        print(message)
        print(f'chirp @ {time.asctime()}')
    except Exception as err:
        print(f'error @ {time.asctime()} : {err}')


def main():
    schedule.every().day.at('12:00').do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
