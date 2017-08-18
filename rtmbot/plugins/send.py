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

class Send(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      user = msg.get("user", "")
      match = re.findall(r"!send( .*)?", text)
      if not match or self.getPermission() is False:
        return
      query = text.split(" ", 1)
      message = query[1]
      userInfo = self.getUserInfo(user)
      return self.sendMessage(channel, message, userInfo)

    def getPermission(self):
      db = fire.database()
      results = db.child('config/send').get()
      return results.val()

    def sendMessage(self, channel, message, userInfo):
      as_user = False
      icon_url = userInfo["user"]["profile"]["image_72"]
      username = userInfo["user"]["profile"]["real_name"]
      result = self.slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=as_user, icon_url=icon_url, username=username)

    def getUserInfo(self, user):
      results = self.slack_client.api_call("users.info", user=user)
      print(results)
      return results
      
