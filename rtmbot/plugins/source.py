from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests

class Source(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!source( .*)?", text)
      if not match:
        return
      message = "https://github.com/garr741/mr_meeseeks\n"
      message = message + "https://github.com/garr741/meeseeks-cloud-functions\n"
      return self.output(channel, message)

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return
