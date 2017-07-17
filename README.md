Mr Meeseeks
=============

Installation
-----------

1. Clone the repo
2. Install rtmbot (ideally into a [virtualenv](https://virtualenv.readthedocs.io/en/latest/))

        pip install rtmbot
        pip install -r requirements.txt

3. Get the ```rtmbot.conf``` , ```secrets.py``` and slack token from TG
4. Change to the rtmbot/ directory and run the 'rtmbot' command to start the bot
5. Please do not test in the public channel. Use #testing-grounds or the Mr Meeseeks DM.

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
