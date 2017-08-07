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

announcements = 'C0HNX7WS2'

class Queue(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      user = msg.get("user", "");
      match = re.findall(r"!announce( .*)?", text)
      if not match:
        return
      results = text.split(" ", 1)
      message = results[1]
      realName = self.whoQueuedIt(user)
      return self.sendMessage(channel, message, user)

    def whoQueuedIt(self, user):
      res1 = self.slack_client.api_call("users.info", user=user)
      return res1["user"]["profile"]["real_name"]

    def sendMessage(self, channel, message):
      self.outputs.append([channel, message])
      
