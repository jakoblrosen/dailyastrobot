import os
import csv
import time
import random
import requests
import schedule
import tweepy

from pathlib import Path
from dotenv import load_dotenv


def get_galaxy():
    with open('info.csv', 'r') as in_file:
        reader = list(csv.reader(in_file))
        random.shuffle(reader)
        reader = iter(reader)
        galaxy = next(reader)
        with open('info.new', 'w') as out_file:
            for row in reader:
                out_file.write(','.join(str(item) for item in row))
                out_file.write('\n')
    os.rename('info.new', 'info.csv')
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
        galaxy_id = galaxy[0]
        galaxy_name = galaxy[1]
        distance = float(galaxy[2])         # stored as Mly
        PHOTO_URL = galaxy[3]
        fname = f'media/{PHOTO_URL.split("/")[-1]}'
        photo = requests.get(PHOTO_URL)
        open(fname, 'wb').write(photo.content)

        NEWLINE = '\n'
        time_to_reach = calculate_time(distance, CURRENT_SPACE_TRAVEL_SPEED)
        message = f'{galaxy_name} ({galaxy_id}){NEWLINE}' \
                  f'Distance: {distance} megalight-years{NEWLINE}' \
                  f'{time_to_reach} years to reach at our current space travel speed'

        media = api.simple_upload(fname)
        api.update_status(status=message, media_ids=[media.media_id])
        print(f'chirp @ {time.asctime()}')
    except Exception as err:
        print(f'error @ {time.asctime()} : {err}')


def main():
    job()
    schedule.every().day.at('12:00').do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
