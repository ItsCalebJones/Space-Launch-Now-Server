
import datetime
from tinydb import TinyDB

db = TinyDB('db.json')


def log(tag, message):
    log_message = ('%s - %s: %s' % ('{:%H:%M:%S %m-%d-%Y}'.format(datetime.datetime.now()), tag, message))
    print log_message
    f = open('spacelaunchnow.log', 'a')
    f.write(log_message + '\n')  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it


def log_error(tag, message):
    log_message = ('ERROR: %s - %s: %s' % ('{:%H:%M:%S %m-%d-%Y}'.format(datetime.datetime.now()), tag, message))
    print log_message
    f = open('spacelaunchnow.log', 'a')
    f.write(log_message + '\n')  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it


def seconds_to_time(seconds):
    seconds_in_day = 86400
    seconds_in_hour = 3600
    seconds_in_minute = 60

    days = seconds // seconds_in_day
    seconds -= days * seconds_in_day

    hours = seconds // seconds_in_hour
    seconds -= hours * seconds_in_hour

    minutes = seconds // seconds_in_minute
    seconds -= minutes * seconds_in_minute
    if days > 0:
        return "{0:.0f} days, {1:.0f} hours, {2:.0f} minutes.".format(days, hours, minutes, seconds)
    elif hours > 0:
        return "{0:.0f} hours, {1:.0f} minutes.".format(hours, minutes, seconds)
    elif minutes > 0:
        return "{0:.0f} minutes.".format(minutes, seconds)