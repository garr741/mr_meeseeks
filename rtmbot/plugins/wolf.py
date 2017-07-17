from __future__ import print_function
from rtmbot.core import Plugin
import json
import re
import requests

class Wolf(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!do( .*)?", text)
      if not match:
        return
      stuff = text.split(" ", 1)
      query = stuff[1]
      return self.wolf(msg, query)

    def wolf(self, msg, text):
      channel = msg.get("channel", "")
      data = {"query": text}
      results = requests.post('https://us-central1-glados-59d2e.cloudfunctions.net/wolframAlpha', data=data)
      return self.outputs.append([channel, results.text])
      