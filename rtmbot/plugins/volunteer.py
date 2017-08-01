from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests

class Volunteer(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!volunteer( .*)?", text)
      if not match:
        return
      link = "https://docs.google.com/forms/d/1CH0SVo7k38lGjBR-_YTHEv7uDWse9_27DKMV60GK9B4/viewform?edit_requested=true"
      return self.output(channel, link)

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return
