from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests

class Template(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!do( .*)?", text)
      if not match:
        return
      return

    def output(self, channel, message):
      #self.outputs.append([channel, message])
      return
