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

class Reporter(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!report( .*)?", text)
      if not match:
        return
      query = text.split(" ", 1)
      eventName = query[1]
      message = self.getEventDetails(eventName) 
      return self.output(channel, message)
      

    def getEventDetails(self, eventName):
      db = fire.database()
      results = db.child("events").child(eventName).get()
      message = ""
      for n in results.each():
        message = message + "*-----" + str(n.key()).upper() + "-----*\n"
        for m in n.val():
          message = message + str(n.val()[m]) + "\n"
      return message

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return
