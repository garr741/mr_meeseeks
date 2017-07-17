from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests

class IdMe(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!id( .*)?", text)
      if not match:
        return
      query = text.split(" ", 1)
      username = query[1]
      username = username[2:-1]
      return self.output(channel, username)

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return
