from tinydb import TinyDB, Query

db = TinyDB('H:\GitHub\Space-Launch-Now-Server\db.json')


class Launch:
    def __init__(self, launch):
        self.launch_id = launch["id"]
        self.launch_name = launch["name"]
        self.status = launch["status"]
        self.net_stamp = launch["netstamp"]
        self.data = launch
        self.notified = False

        if len(launch["location"]["pads"]) > 0:
            self.location = launch["location"]["pads"][0]["name"]

        if len(launch["missions"]) > 0:
            self.missions = launch["missions"]

        self.twitter_table = db.table('twitter')

        response = self.twitter_table.search(Query().launch == self.launch_id)
        if len(response) > 0:
            self.last_twitter_post = response[len(response) - 1]['last_twitter_update']
        else:
            self.last_twitter_post = None

        self.launch_table = db.table('launch')

        launch_cache = self.launch_table.search(Query().launch == self.launch_id)
        if launch_cache:
            self.wasNotifiedTwentyFourHour = launch_cache[0]['isNotified24']
            self.wasNotifiedOneHour = launch_cache[0]['isNotifiedOne']
            self.wasNotifiedTenMinutes = launch_cache[0]['isNotifiedTen']
            self.notified = launch_cache[0]['notified']

    def reset_notifiers(self):
        self.wasNotifiedTwentyFourHour = False
        self.wasNotifiedOneHour = False
        self.wasNotifiedTenMinutes = False
        self.update_record()

    def is_notified_24(self, boolean):
        self.wasNotifiedTwentyFourHour = boolean
        self.update_record()

    def is_notified_one_hour(self, boolean):
        self.wasNotifiedOneHour = boolean
        self.update_record()

    def is_notified_ten_minutes(self, boolean):
        self.wasNotifiedTenMinutes = boolean
        self.update_record()

    def update_record(self):
        if self.notified is False:
            self.notified = True
            self.launch_table.insert({'launch': self.launch_id,
                                      'isNotified24': self.wasNotifiedTwentyFourHour,
                                      'isNotifiedOne': self.wasNotifiedOneHour,
                                      'isNotifiedTen': self.wasNotifiedTenMinutes, 'notified': self.notified})
        else:
            self.launch_table.update({'isNotified24': self.wasNotifiedTwentyFourHour,
                                      'isNotifiedOne': self.wasNotifiedOneHour,
                                      'isNotifiedTen': self.wasNotifiedTenMinutes, 'notified': self.notified},
                                     Query().launch == self.launch_id)


