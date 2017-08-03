from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests
import pyrebase
from secrets import secrets

firebaseConfig = secrets["firebase"]

fire = pyrebase.initialize_app(firebaseConfig)

class Jira(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"(?i)nm-[0-9]{0,4}", text)
      if not match:
        return
      if self.getPermission() is False:
        return
      return self.convert(channel, match[0])

    def output(self, channel, message):
      self.outputs.append([channel, message])

    def convert(self, channel, query):
      message = "https://angieslist.atlassian.net/browse/" + query
      self.output(channel, message)

    def getPermission(self):
      db = fire.database()
      results = db.child('config/jira').get()
      return results.val()
