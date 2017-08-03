from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests
import random
from hmm import hmm
import pyrebase
from secrets import secrets

firebaseConfig = secrets["firebase"]

fire = pyrebase.initialize_app(firebaseConfig)

class Hmmm(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      user = msg.get("user", "");
      match = re.findall(r"^hm{2,4}?", text)
      if not match:
        return
      if self.getPermission() is False:
        return
      response = self.randomelt(hmm)
      return self.output(channel, response)

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return

    def randomelt(self, dic):
      i = random.randint(0, len(dic) - 1)
      return dic[i]

    def getPermission(self):
      db = fire.database()
      results = db.child('config/hmm').get()
      return results.val()
