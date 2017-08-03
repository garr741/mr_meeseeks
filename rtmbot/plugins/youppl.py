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

class Youppl(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"you (people|ppl)( .*)?", text)
      if not match:
        return
      if self.getPermission() is False:
        return
      link = "https://media0.giphy.com/media/13VSAbTVuYJfLa/giphy.gif"
      return self.output(channel, link)

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return

    def getPermission(self):
      db = fire.database()
      results = db.child('config/youppl').get()
      return results.val()
