#!/usr/bin/env python3

import sys
import logging
from threading import Thread
from datetime import datetime
from time import sleep

from flightplan import parse


def init_env_data():
    pass


def execute_flightplan(fp):
    for ins, args in fp:
        ins(logging, *args)
    print('done')


def collect_sensor_data():
    pass


def update_env_data():
    pass


def forward_sensor_data():
    pass


def main(flightplan):
    '''
    The main loop running while the drone is in flight.

    parse given flight-plan
    initialize environment data

    while flightplan:
        take sensor data
        process sensor data
        update flight controller(flightplan, sensor data)
        forward sensor data to hub
    '''

    fp = parse(flightplan)

    init_env_data()

    threads = [
        Thread(target=execute_flightplan,  args=[fp]),
        Thread(target=collect_sensor_data, args=[]),
        Thread(target=forward_sensor_data, args=[])
    ]

    for t in threads:
        t.start()

if __name__ == '__main__':

    time = datetime.now()

    logging.basicConfig(
        filename='logs/{}.log'.format(time.strftime('%d-%m-%Y_%H:%M:%S')),
        filemode='w+',
        format='%(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    logging.info('Program begins {}'.format(time.strftime('%d-%m-%Y %H:%M:%S')))

    try:
        with open(sys.argv[1], 'r') as f:
            main(f.read())

    except IndexError:
        logging.error('No flight-plan given. Shutting down.')
    except FileNotFoundError:
        logging.error('Flight-plan does not exist. Shutting down.')
