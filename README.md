Mr Meeseeks
=============

Installation
-----------

1. Clone the repo
2. Install rtmbot (ideally into a [virtualenv](https://virtualenv.readthedocs.io/en/latest/))

        pip install rtmbot
        pip install -r requirements.txt

3. Get the rtmbot.conf and slack token file from Me
4. Change to the rtmbot/ directory and run the 'rtmbot' command to start the bot

For example, if your python path includes '/path/to/myproject' and you include `plugins.repeat.RepeatPlugin` in ACTIVE_PLUGINS, it will find the RepeatPlugin class within /path/to/myproject/plugins/repeat.py and instantiate it, then attach it to your running RTMBot.

A Word on Structure
-------
To give you a quick sense of how this library is structured, there is a RtmBot class which does the setup and handles input and outputs of messages. It will also search for and register Plugins within the specified directory(ies). These Plugins handle different message types with various methods and can also register periodic Jobs which will be executed by the Plugins.
```
RtmBot
├── Plugin
|      ├── Job
|      └── Job
├── Plugin
└── Plugin
       └── Job
```

Add Plugins/Commands
-------

To add a plugin, copy the ```template.py``` file in the ```plugins/``` directory to a new file. Add that new plugin to the ```rtmbot.conf``` file.

##### RTM Output
Plugins can send messages back to any channel or direct message. This is done by appending a two item array to the Plugin's output array (```myPluginInstance.output```). The first item in the array is the channel or DM ID and the second is the message text. Example that writes "hello world" when the plugin is started:

    class myPlugin(Plugin):

        def process_message(self, data):
            self.outputs.append(["C12345667", "hello world"])

##### SlackClient Web API Output
Plugins also have access to the connected SlackClient instance for more complex output (or to fetch data you may need).

    def process_message(self, data):
        self.slack_client.api_call(
            "chat.postMessage", channel="#general", text="Hello from Python! :tada:",
            username="pybot", icon_emoji=":robot_face:"


#### Timed jobs
Plugins can also run methods on a schedule. This allows a plugin to poll for updates or perform housekeeping during its lifetime. Jobs define a run() method and return any outputs to be sent to channels. They also have access to a SlackClient instance that allows them to make calls to the Slack Web API.

For example, this will print "hello world" every 10 seconds. You can output multiple messages two the same or different channels by passing multiple pairs of [Channel, Message] combos.

    from core import Plugin, Job


    class myJob(Job):

        def run(self, slack_client):
            return [["C12345667", "hello world"]]


    class myPlugin(Plugin):

        def register_jobs(self):
            job = myJob(10, debug=True)
            self.jobs.append(job)