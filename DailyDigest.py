from apscheduler.schedulers.blocking import BlockingScheduler
from twitter import *
from libraries.launchlibrarysdk import LaunchLibrarySDK
from libraries.onesignalsdk import OneSignalSdk
from models.models import Launch
from utils.config import keys
from utils.util import db, log

AUTH_TOKEN_HERE = keys['AUTH_TOKEN_HERE']
APP_ID = keys['APP_ID']
DAEMON_SLEEP = 6000
TAG = 'Digest Server'


def run_daily():
    log(TAG, 'Running Daily Digest - Daily...')
    daily_digest = DailyDigestServer()
    daily_digest.run(daily=True)


def run_weekly():
    log(TAG, 'Running Daily Digest - Weekly...')
    daily_digest = DailyDigestServer()
    daily_digest.run(weekly=True)


class DailyDigestServer:
    def __init__(self):
        self.one_signal = OneSignalSdk(AUTH_TOKEN_HERE, APP_ID)
        self.launchLibrary = LaunchLibrarySDK()
        response = self.one_signal.get_app(APP_ID)
        assert response.status_code == 200
        self.app = response.json()
        assert isinstance(self.app, dict)
        assert self.app['id'] and self.app['name'] and self.app['updated_at'] and self.app['created_at']
        self.app_auth_key = self.app['basic_auth_key']
        self.twitter = Twitter(
            auth=OAuth(keys['TOKEN_KEY'], keys['TOKEN_SECRET'], keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
        )
        self.launch_table = db.table('launch')
        self.time_to_next_launch = None
        self.next_launch = None

    def run(self, daily=False, weekly=False):
        """The daemon's main loop for doing work"""
        if daily:
            self.check_launch_daily()
        if weekly:
            self.check_launch_weekly()

    def check_launch_daily(self):
        launch_data = self.launchLibrary.get_next_launches().json()['launches']
        launches = []
        for launch_instance in launch_data:
            launch = Launch(launch_instance)
            if launch.status == 1:
                launches.append(launch)
                log(TAG, launches)

    def check_launch_weekly(self):
        launch_data = self.launchLibrary.get_next_launches().json()['launches']
        log(TAG, launch_data)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    run_daily()
    scheduler.add_job(run_daily, trigger='cron', day_of_week='mon-sun', hour=8, minute=30)
    scheduler.add_job(run_weekly, trigger='cron', day_of_week='fri', hour=12, minute=30)
    scheduler.print_jobs()
    scheduler.start()