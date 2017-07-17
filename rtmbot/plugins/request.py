from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests

class Request(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      user = msg.get("user", "")
      match = re.findall(r"!request( .*)?", text)
      message = "Ooohhh can do."
      return self.requestIt(channel, userName, match[0])

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return

    def requestIt(self, channel, userName, request):
      
      self.output(channel, message)
      
