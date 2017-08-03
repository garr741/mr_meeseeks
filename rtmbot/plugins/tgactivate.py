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

class TGActivate(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!init( .*)?", text)
      if not match:
        return
      return self.createSomething()

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return

    def createUserList(self, channel):
      results = self.slack_client.api_call("users.list")
      db = fire.database()
      for n in results["members"]:
       db.child("users/" + n["id"]).set(n)
      return self.output(channel, "Ooohhh can do.")

    def updateUserListWithDMIDS(self, channel):
      db = fire.database()
      user = db.child("users").get()
      for n in user.each():
        username = n.val()['id']
        results = self.slack_client.api_call("im.open", user=username)
        if results["ok"] is True:
          db.child("users").child(username).update({"dmIM": results["channel"]["id"]})
      return self.output(channel, "Ooohhh can do.")

    def createSomething(self):
      db = fire.database()
      db.child("data/presence").set({'enabled': False})
