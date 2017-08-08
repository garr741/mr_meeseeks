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
        self.deleteMessage(channel, ts)
      return

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return

    def deleteMessage(self, channel, ts):
      data = {"channel": channel, 'ts': ts}
      results = requests.post('https://us-central1-glados-59d2e.cloudfunctions.net/deleteMessage', data=data)

    def getChannel(self):
      db = fire.database()
      results = db.child('config/announceChannel').get()
      return results.val()

    def getPermission(self):
      db = fire.database()
      results = db.child('config/autodelete').get()
      return results.val()
      

