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

class Request(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      user = msg.get("user", "")
      match = re.findall(r"!request( .*)?", text)
      if not match:
        return
      if self.getPermission() is False:
        return
      message = "Ooohhh can do."
      return self.output(channel, message)

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return

    def getPermission(self):
      db = fire.database()
      results = db.child('config/request').get()
      return results.val()
      
