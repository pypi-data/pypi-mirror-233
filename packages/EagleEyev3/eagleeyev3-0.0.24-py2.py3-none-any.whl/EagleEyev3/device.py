
import json
import logging
import requests

from datetime import datetime, timedelta
from pytz import timezone

from io import BytesIO

logging.basicConfig(level=logging.INFO)




class Device():

    def __init__(self, id=None, name=None, status=dict(), account_id=None, user_base_url=None, een_instance=None):

        self.id = id
        self.name = name
        self.status = status
        self.account_id = account_id
        self.user_base_url = user_base_url,
        self.een_instance = een_instance

    def get_id(self):
        return self.id

    def get_status(self):
        if 'connectionStatus' in self.status:
            return self.status['connectionStatus']
        return None

    def is_online(self):
        if 'connectionStatus' in self.status:
            return self.status['connectionStatus'] == "online"
        return None

    def is_offline(self):
        if 'connectionStatus' in self.status:
            return self.status['connectionStatus'] != "online"
        return None

    def __repr__(self):
        if self.is_online():
            online = '✅'
        elif self.is_offline():
            online = '❌'
        else:
            online = '？'
        return f"{online} [{self.id}] - {self.name}"













