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

class Vote(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!vote (help|start|stop|unexcused|excused|info)( .*)?", text)
      if not match:
        return
      query = text.split(" ", 1)
      eventName = query[1]
      return self.output(channel, eventName)

    def getPermission(self):
      db = fire.database()
      results = db.child('vote/enabled').get()
      return results.val()

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return
    