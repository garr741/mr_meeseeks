from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests
import time
import pyrebase
import os
import uuid
from secrets import secrets

firebaseConfig = secrets["firebase"]

fire = pyrebase.initialize_app(firebaseConfig)

class Blast(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "")
      match = re.findall(r"!blast( .*)?", text)
      if not match:
        return
      query = text.split(" ", 1)
      message = query[1]
      if self.getPermission() is True:
        users = self.getUsers()
        eventId = str(uuid.uuid4().fields[-1])[:5]
        self.createEvent(eventId, message)
        self.distribute(users, message, eventId)
        self.output(channel, "Done: `" + eventId + "`")
      else:
        self.output(channel, "Who's there?")
        return

    def distribute(self, users, message, eventId):
      for n in users:
        self.sendMessage(n, message, eventId)

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
      return userList

    def sendMessage(self, channel, message, eventId):
      as_user = True
      attachments = [{'text': '', 'callback_id': 'knockknock~' + eventId, 'color': '#36a64f', 'actions': [{'name': 'Yes', 'text': 'Yes', 'type': 'button', 'value': 'Yes', 'style': 'primary'}, {'name': 'No', 'text': 'No', 'type': 'button', 'value': 'No', 'style': 'danger'}, {'name': 'Maybe', 'text': 'Maybe', 'type': 'button', 'value': 'Maybe'}]}]
      result = self.slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=as_user, attachments=json.dumps(attachments))

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return

    def getPermission(self):
      db = fire.database()
      results = db.child('config/blast').get()
      return results.val()

    def createEvent(self, eventId, message):
      db = fire.database()
      obj = { 'message': message}
      results = db.child('events').child(eventId).push(obj)
