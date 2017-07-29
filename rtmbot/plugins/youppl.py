from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests

class Youppl(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"you (people|ppl)( .*)?", text)
      if not match:
        return
      link = "https://media0.giphy.com/media/13VSAbTVuYJfLa/giphy.gif"
      return self.output(channel, link)

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return
