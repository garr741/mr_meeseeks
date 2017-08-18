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

class AutoDelete(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      user = msg.get("user", "");
      ts = msg.get("ts", "")
      thread_ts = msg.get("thread_ts", None)
      subtype = msg.get("subtype", None)
      if self.getChannel() == channel and self.getPermission() and thread_ts is None and subtype is None:
        self.deleteMessage(channel, ts, user, text)
      return 

    def deleteMessage(self, channel, ts, user, text):
      data = {"channel": channel, 'ts': ts}
      results = requests.post('https://us-central1-glados-59d2e.cloudfunctions.net/deleteMessage', data=data)
      self.notifyUser(user, text)

    def getChannel(self):
      db = fire.database()
      results = db.child('config/autodeleteChannel').get()
      return results.val()

    def getPermission(self):
      db = fire.database()
      results = db.child('config/autodelete').get()
      return results.val()

    def notifyUser(self, user, text):
      message = "Hi, your message was autodeleted. Posting in #announcements is not allowed.\n\n"
      message = message + "Please use the slash command `/announce help` for more information about making an announcement or "
      message = message + "reply using a Thread for follow-up questions/comments\n\n\n"
      message = message + "> " + text
      result = self.slack_client.api_call("chat.postMessage", channel=user, text=message)

      

