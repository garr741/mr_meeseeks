from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests
import time
import pyrebase
import os
from secrets import secrets

firebaseConfig = secrets["firebase"]

fire = pyrebase.initialize_app(firebaseConfig)


class KnockKnock(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "")
      match = re.findall(r"!knockknock( .*)?", text)
      if not match:
        return
      query = text.split(" ", 1)
      eventName = query[1]
      #users = self.getUsers()
      self.distribute(channel, eventName)
      self.output(channel, "Done!")

    def distribute(self, users, eventName):
      # for n in users:
      #   self.sendMessage(n, eventName)
      self.sendMessage(users, eventName)

    def getUsers(self):
      db = fire.database()
      userList = []
      user = db.child("users").get()
      for n in user.each():
        try:
          dmInfo = n.val()["dmIM"]
          userList.append(dmInfo)
        except Exception as e:
          pass
      #return userList

    def sendMessage(self, channel, eventName):
      message = "Hi, the " + eventName + " is coming up soon!"
      as_user = True
      attachments = [{'text': 'Will you be able to attend?', 'callback_id': 'knockknock~' + eventName, 'color': '#36a64f', 'actions': [{'name': 'Yes', 'text': 'Yes', 'type': 'button', 'value': 'Yes', 'style': 'primary'}, {'name': 'No', 'text': 'No', 'type': 'button', 'value': 'No', 'style': 'danger'}, {'name': 'Maybe', 'text': 'Maybe', 'type': 'button', 'value': 'Maybe'}]}]
      result = self.slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=as_user, attachments=json.dumps(attachments))

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return