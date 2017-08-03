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

class Inspire(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!inspire(.*)?", text)
      if not match:
        return
      if self.getPermission() is False:
        return
      return self.inspire(channel)

    def inspire(self, channel):
      results = requests.get("http://inspirobot.me/api?generate=true")
      self.output(channel, results.text)
      return

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return

    def getPermission(self):
      db = fire.database()
      results = db.child('config/inspire').get()
      return results.val()
