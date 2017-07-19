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

class Logger(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      user = msg.get("user", "");
      ts = msg.get("ts", "")
      if user == "":
        return
      if text == "":
        return
      res1 = self.slack_client.api_call("users.info", user=user)
      userName = res1["user"]["profile"]["real_name"]
      channelName = ""
      if channel.startswith("C"):
        res2 = self.slack_client.api_call("channels.info", channel=channel)
        channelName = res2["channel"]["name"]
        db = fire.database()
        db.child("Messages").child(channelName).push({'user': userName, 'text': text, 'ts': ts})
      