from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests
import random
from quotes import quotes


class Status(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      user = msg.get("user", "");
      match = re.findall(r"!status( .*)?", text)
      if not match:
        return
      res = self.slack_client.api_call("users.info", user=user)
      userName = res["user"]["profile"]["first_name"]
      response = self.randomelt(quotes)
      return self.output(channel, response)

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return

    def randomelt(self, dic):
      i = random.randint(0, len(dic) - 1)
      return dic[i]
