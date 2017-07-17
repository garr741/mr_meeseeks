from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests

class Help(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!help(.*)?", text)
      if not match:
        return
      return self.helpme(channel)

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return

    def helpme(self, channel):
      message = ("```" + 
                "!do <question> - returns the answer to your question, or it doesn't who knows? (ex !do 3*7) (ex !do Barack Obama's birthday)\n" +
                "!inspire - generates a random inspiration courtesy of inspirobot\n" + 
                "!calendar - list the next three events on the Tech Fellowship Calendar!\n" + 
                "```")
      self.output(channel, message)
