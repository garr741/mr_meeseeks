from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
from dateutil.parser import parse
from datetime import date, timedelta, datetime
import json
import re
import requests
import dateutil.parser
import calendar
import pyrebase
from secrets import secrets

firebaseConfig = secrets["firebase"]

fire = pyrebase.initialize_app(firebaseConfig)

calendarId = secrets["google"]["calendarId"]
apiKey = secrets["google"]["apiKey"]

class CalendarBot(Plugin):
  
    def process_message(self, msg):
      text = msg.get("text", "")
      channel = msg.get("channel", "");
      match = re.findall(r"!calendar( .*)?", text)
      if not match:
        return
      if self.getPermission() is False:
        return
      nextEvents = self.getEvents(channel)
      self.sortEvents(channel, nextEvents)
      return

    def output(self, channel, message):
      self.outputs.append([channel, message])
      return

    def getEvents(self, channel):
      url = "https://www.googleapis.com/calendar/v3/calendars/" + calendarId + "/events/?key=" + apiKey
      results = requests.get(url)
      i = 0
      nextEvents = []
      for n in results.json()["items"]:
        if n["status"] == "confirmed":
          theDate = ""
          checker = date.today() - timedelta(1)
          yesterday = datetime(checker.year, checker.month, checker.day)
          try:
            theDate = parse(n["start"]["dateTime"])
            if datetime(theDate.year, theDate.month, theDate.day) > yesterday:
              nextEvents.append(n)
          except Exception as e:
            theDate = parse(n["start"]["date"])
            if datetime(theDate.year, theDate.month, theDate.day) > yesterday:
              nextEvents.append(n)
      return nextEvents

    def sortEvents(self, channel, nextEvents):
      threeEvents = sorted(nextEvents, key=self.dateHelper)
      message = "Here are the next three events!\n\n"
      for i in range(0,3):
        message = message + "> *" + threeEvents[i]["summary"] + "*\n"
        theDate = parse(self.dateHelper(threeEvents[i]))
        message = message + "> " + self.dateFormatter(theDate) + "\n"
        hour = theDate.time().hour
        minute = theDate.time().minute
        if minute is 0:
          minute = "00"
        if hour > 12 is not 0:
          message = message + "> Starting at: " + str(hour - 12) + ":" + str(minute) + " PM\n"
        elif hour < 12 and hour is not 0:
          message = message + "> Starting at: " + str(hour) + ":" + str(minute) + " AM\n"
        try:
            message = message + "> Located at: " + threeEvents[i]["location"] + "\n"
        except Exception as e:
            pass
        message = message + "\n"
      self.output(channel, message)
      return threeEvents

    def dateHelper(self, event):
      try:
        return event["start"]["date"]
      except Exception as e:
        return event["start"]["dateTime"]

    def dateFormatter(self, date):
      month = calendar.month_name[date.month]
      weekday = calendar.day_name[date.weekday()]
      day = date.day
      year = date.year
      results = str(weekday) + ", " + str(month) + " " + str(day) + ", " + str(year)
      return results

    def getPermission(self):
      db = fire.database()
      results = db.child('config/calendar').get()
      return results.val()
        