from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests
import sys
import os
import signal

class Kill(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!kill( .*)?", text)
      if not match:
        return
      return self.kill(msg)

    def outputs(self, channel, message):
      self.outputs.append([channel, message])
      return

    def kill(self, msg):
      channel = msg.get("channel", "")
      user = msg.get("user", "")
      response = "lol, nice try"
      if user == "U0HSH61K7":
        pid = os.getpid()
        os.kill(int(pid), signal.SIGTERM)
      return self.output(channel, response)
