#! /Users/jslater/anaconda3/bin/python
# $Id: dnd.py 2015-04-27 19:05:00Z  $
# Author: Joseph Slater <joseph.slater@wright.edu>
# Copyright: This script has been placed in the public domain.
# Version 1.2: Added help via --help and -h
# Version 1.1: Added ability to set by time.

import sys
import os
import subprocess
import time
from tkinter import *

"""
Changed Notification Center status on Mac to "Do not disturb" for
a) n minutes, (n>4)
b) or n hours. (n<=4)
c) or until n time where n is in hour:minute format using 12 hour clock.

The concept of the split mode is that since Notification Center has a built-in
timer of 24 hours (1 day), usage of this script will be limited to 1/2 day or
less. Any longer... modify the script or just turn it off manually?
"""
# print(print_help())

__docformat__ = 'reStructuredText'

# I should have used argparse: https://docs.python.org/3/library/argparse.html

import logging
# set your log level
logging.basicConfig(level=logging.ERROR)
# logging.basicConfig(level=logging.DEBUG)
logging.debug('This is a log message')

os.environ['PATH'] = os.path.normpath(
    os.environ['PATH'] + ':/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin:')

a1 = subprocess.check_output(
    ['defaults -currentHost write ~/Library/Preferences/ByHost/com.apple.notificationcenterui doNotDisturb -boolean true'], shell=True)

a = subprocess.check_output(['date -u +"%Y-%m-%d %H:%M:%S +0000"'], shell=True)
b = a.decode('utf-8')

a2 = subprocess.Popen(
    ['defaults -currentHost write ~/Library/Preferences/ByHost/com.apple.notificationcenterui doNotDisturbDate -date "' + b + '"'], shell=True)

logging.info('Info only. Debug mode')
#logging.warning('Warning only')

a3 = subprocess.Popen(['killall NotificationCenter'], shell=True)

curhour = time.localtime().tm_hour
curmin = time.localtime().tm_min
logging.debug(curhour)
logging.debug(curmin)

if sys.argv.__len__() == 1:
    endtime = input('When do you want silence to end? ')
    logging.debug(endtime)
else:
    endtime = sys.argv[1]

if endtime == '--help' or endtime == '-h':
    print("Changed Notification Center status on Mac to 'Do not disturb' for: \n\
    a) n minutes, (n>4)\n\
    b) or n hours. (n<=4)\n\
    c) or until n time where n is in hour:minute format using 12 hour clock.\n\
    The concept of the split mode is that since Notification Center has a built-in timer of 24 hours\
    (1 day), usage of this script will be limited to 1/2 day or less.")

    sys.exit()
elif str.find(endtime, ':') != -1:
    colloc = str.find(endtime, ':')
    hour = float(endtime[:colloc])
    min = float(endtime[(colloc + 1):])
    logging.debug(hour)
    logging.debug(min)
    if hour < 7:
        hour = hour + 12
    numin = (hour - curhour) * 60 + (min - curmin)

else:
    numin = float(endtime)
    if numin < 4.01:
        numin = numin * 60

    colloc = 0

logging.debug('Plan on sleeping for this many minutes.')
logging.debug(numin)

if numin > 4.01 or colloc != 0:
    a5 = subprocess.Popen(['killall sleep -s;sleep ' + str(numin * 60) + ';defaults -currentHost write \
                     ~/Library/Preferences/ByHost/com.apple.notificationcenterui doNotDisturb -boolean false; \
                     defaults -currentHost delete ~/Library/Preferences/ByHost/com.apple.notificationcenterui \
                     doNotDisturbDate; killall NotificationCenter'], shell=True)
    print('Sleeping for ' + str(numin) + ' min.')
    logging.debug('Minute Mode')
else:
    a5 = subprocess.Popen(['sleep ' + str(numin * 3600) + ';defaults -currentHost write \
                     ~/Library/Preferences/ByHost/com.apple.notificationcenterui doNotDisturb -boolean false; \
                     defaults -currentHost delete ~/Library/Preferences/ByHost/com.apple.notificationcenterui \
                     doNotDisturbDate; killall NotificationCenter'], shell=True)
    numin = numin
    logging.debug('Sleeping for ' + str(numin) + ' min.')
    logging.warning(
        'Hour Mode- to never be entered again! Please report this error.')

wakehour = curhour
logging.debug('wakehour temp')
logging.debug(wakehour)

wakemin = numin + curmin

logging.debug('wakemin temp')
logging.debug(wakemin)

while wakemin > 59:
    logging.debug('swapping min for hour')
    wakemin = wakemin - 60
    logging.debug(wakemin)
    wakehour = wakehour + 1
    logging.debug(wakehour)

strwakemin = str(wakemin)

if wakehour > 12:
    wakehour = wakehour - 12

logging.debug(strwakemin)
logging.debug(str.find(strwakemin, '.'))
if str.find(strwakemin, '.') == 1:
    strwakemin = '0' + strwakemin
    logging.debug(strwakemin)

print('Do not disturb set until ' + str(wakehour) + ':' + strwakemin[:2]
      + '. (' + str(numin)[:-2] + ' minutes.)')
