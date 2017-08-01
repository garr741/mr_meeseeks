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

allowed = True

class TGTest(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!tgtest( .*)?", text)
      if not match:
        return
      if self.getResults() is True:
        self.sendSingleMessage(channel, "MM")
      return 

    def sendSingleMessage(self, channel, eventName):
      message = "Hi, the " + eventName + " is coming up soon!"
      as_user = True
      attachments = [{'text': 'Choose an option!', 'callback_id': 'tester~' + eventName, 'color': '#36a64f', 'actions': [{'name': 'Yes', 'text': 'Yes', 'type': 'button', 'value': 'Yes', 'style': 'primary'}, {'name': 'No', 'text': 'No', 'type': 'button', 'value': 'No', 'style': 'danger'}]}]
      result = self.slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=as_user, attachments=json.dumps(attachments))

    def getResults(self):
      db = fire.database()
      results = db.child('config/tgtest').get()
      return results.val()
      
