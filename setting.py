#!/usr/bin/env python
# -*-coding:UTF-8-*-
import logging
import os

####################################################

cur_path = os.path.dirname(os.path.abspath(__file__))

DEBUG = False

if os.path.exists(os.path.join(cur_path, '__test__')):
    DEBUG = True

LOG_FILENAME = 'live_god.log'

if DEBUG:
    LOG_LEVEL = logging.DEBUG
    LOG_PATH = ''
    logging.info('log mode is debug ...')
    logging.info('log file is in current directory called '+LOG_FILENAME+'. Good work!\n')
else:
    LOG_LEVEL = logging.WARNING
    LOG_PATH = '/var/log/'
    logging.info('log mode is warning ...')
    logging.info('log file is in '+LOG_PATH+' directory called '+LOG_FILENAME+'. Good work!\n')