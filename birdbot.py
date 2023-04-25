import os
import math
import time
import logging
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

    couch = couchdb.Server(f'http://{os.getenv("COUCH_USER")}:{os.getenv("COUCH_PASSWORD")}'
                           f'@{os.getenv("COUCH_HOST")}:{os.getenv("COUCH_PORT")}')
    db = couch['dailyastrobotdb']
    galaxy_ids = [id for id in db]
    galaxy_id = random.choice(galaxy_ids)
    galaxy = dict(db[galaxy_id].items())
    del db[galaxy_id]
    return galaxy


# calculate time in years given distance in Mly and speed in km/h
def calculate_time(distance, speed):
    km_to_mly = 1.0577e-19
    h_to_y = 1.1415e-4
    delta = distance / (speed * (km_to_mly / h_to_y))
    return int(delta)


# calculate relativistic time given time and percentage of speed of light
def calculate_relative_time(delta, c_percent):
    return int(delta * math.sqrt(1 - c_percent ** 2))


def job():
    dotenv_path = Path('secrets.env')
    load_dotenv(dotenv_path=dotenv_path)

    auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)

    current_space_travel_speed = 6.92e5  # stored as km/h
    log = logging.getLogger('dailyastrobot')

    try:
        galaxy = get_galaxy()
        galaxy_name = galaxy.get('name')
        galaxy_code = galaxy.get('code')
        distance = galaxy.get('distance')
        image_url = galaxy.get('image_url')
        fname = f'media/{image_url.split("/")[-1]}'
        photo = requests.get(image_url)
        open(fname, 'wb').write(photo.content)

        time_to_reach = calculate_time(distance, current_space_travel_speed)
        time_to_reach_relative = calculate_relative_time(time_to_reach, 0.999)
        message = (f'{galaxy_name} ({galaxy_code})\n'
                   f'Distance: {distance} megalight-years\n'
                   f'{int(time_to_reach / 1e9)} billion years to reach at our current space travel speed\n'
                   f'{int(time_to_reach_relative / 1e6)} million years to reach at 99.9% the speed of light')

        media = api.simple_upload(fname)
        api.update_status(status=message, media_ids=[media.media_id])
        log.info(f'chirp @ {time.asctime()}')
    except Exception as err:
        log.warning(f'error @ {time.asctime()} : {err}')


def main():
    logging.Logger('dailyastrobot')
    schedule.every().day.at('12:00').do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
