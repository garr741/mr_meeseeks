from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import json
import re
import requests

announcements = 'C0HNX7WS2'

class ChannelInfo(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!channel( .*)?", text)
      if not match:
        return
      message = self.getChannelInfo(channel)
      self.output(channel, message)


    def getChannelInfo(self, channel):
      res2 = self.slack_client.api_call("channels.info", channel=channel)
      return res2["channel"]["id"]

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return
