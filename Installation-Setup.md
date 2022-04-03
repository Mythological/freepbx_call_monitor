### Installation Steps
1) [Obtain MySQL Password for freepbxuser from MySQL](Installation-Setup.md#get-freepbxuser-mysql-password)
2) [Obtain API Keys/Webhook URL ](Installation-Setup.md#messaging-services)
3) [Install needed packages, clone Repo and install library dependencies](Installation-Setup.md#installing-the-script)
4) [Configure the script](Installation-Setup.md#configure-the-script)
5) [Run the Script](Installation-Setup.md#running-the-script)

---

### Get freepbxuser MySQL Password

Since this is your server you are running this on, you will need to obtain the MySQL Password for the freepbxuser account. 

This should be relatively easy. 

- SSH/Log into the terminal of your FreePBX Server.
- Run the following command:
```bash
cat /etc/freepbx.conf
```

- You want the key that is between the single quotes on the line that looks like this:
```php
$amp_conf['AMPDBPASS'] = 'COPY THE KEY THAT IS HERE BETWEEN THESE QUOTES'
```

- Copy this somewhere as you will need it for the script.

---

### Messaging Services

Here we need to setup the service you want to get the notifications from.

#### Discord Webhook URL

If you will be using Discord, you will need to configure your Discord server.

- Create a new text channel for the bot (I called mine #pbx-alerts).
- Go to the settings of your server and click on integrations (right click the server icon and go to server settings and then integrations).
- In the middle of the screen should be a button that says "Create Webhook". Click that.
- Give it a name (I used FreePBX for mine) and select the new text channel you just created, or use an existing channel if you like.
- Click the "Copy Webhook URL" button at the bottom of the window. Paste this somewhere as you will need it here shortly again. (If loose it, you can come back later after creation and click the Copy button again).
- Click "Save". Your Webhook and Channel are ready.

#### Telegram

* If you plan on using Telegram:
    - You will need to first either create a Telegram bot or use an existing one you own. If this is your first bot, you can use the [steps here](https://core.telegram.org/bots#6-botfather) and talk to @BotFather to create your bot. You will need the bot token for the bot you are using/creating and this can also be obtained from talking to @BotFather.
    - You will also need your chatid. This can be obtained once your bot is up and running by sending a message to your bot and using the Telegram API by going to this url: [https://api.telegram.org/bot'API-access-token'/getUpdates?offset=0](https://api.telegram.org/bot<API-access-token>/getUpdates?offset=0) replacing 'API-access-token' with your bot access token you obtained in the previous step. You will see some json and you will be able to find your ID there in the From stanza.
    - Note that Influx DB provides some examples of what to look for in the above 2 steps. You can go to their page by [clicking here](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/).

#### Mattermost

* If you plan on using Mattermost, you will either need to have an existing server or spin up a new one for use of you and your familiy and friends. These steps assume you already have a server ready to go.
* Note: you will need admin access to create the Webhook Integration.
* There are a few more steps involved in setting up the Mattermost Webhook:
  - First you will need to create a new channel for the bot to post to (I called mine FreePBX)
  - Next, go to the hamburger menu by your name and scroll down to Integrations.
  - Here you will want to click Incoming Webhooks
  - Click "Add Incoming Hook" and then fill out the form provided. You will want to select your FreePBX channel and lock the bot to that channel.
  - Once you click create, a new webhook is born. The URL will be made up of two parts
    - The URL is the domain of your Mattermost server. So for example myserver.mattermost.com
    - The API key is the mix of Letter and numbers after the /hook/ part of the url showing.
  - You will need to put both of these parts into the configuration file to be able to send to a Mattermost Webhook.

#### Pushover

* Pushover is a service that sends notifications to your phone, tablet and computer.
* **It is important to note that, while they have a free trial, it is a paid service. It is $4.99 for every platform you want to use it on after a 30 Day trial, but you only pay that $4.99 once for every platform you are using it on.**
* This is the only paid service that this app supports.
* While I am not advocating buying the service, I know that some people use it for other things already and it was an easy add to the program.
* More information about Pushover can be found [here](https://pushover.net/).
* To get your API keys for Pushover:
  * Log into your Pushover account.
  * Your User Key is the in the upper right hand corner of the screen there. Copy that someplace.
  * Next, you will need to register for an API key for Pushover to use the application with. Scroll to the bottom where it says "Your Applications" and click "Create and Application/API Token"
  * Give it a name, agree to the TOS and click create application.
  * On the next screen it shows you the API Key you will need. Copy that out and now you have the two pieces you need for message notifications to work with Pushover.


#### Slack

Like Mattermost, Slack uses Webhook URLs to allow incoming data to be posted to a channel.

* If you plan on using Slack, you will either need to have an existing server or spin up a new one for use of you and your familiy and friends. These steps assume you already have a server ready to go.
* Note: you will need admin access to create the Webhook Integration.
* Create new channel in Slack (ex. FreePBX)
* Click on Apps and then search for "incoming Webhook"
* Click on Add and a browser window will open.
* It will ask you to choose the server/channel to post to. Then Create the Webhook.
* Scroll down the next page down to integration settings. 
  * Double check the channel is correct
  * Copy the Webhook URL since you will need that later.
  * Give it a name (ex. FreePBX)
  * You can upload an Icon if you want.
  * Click Save. This will generate your incoming webhook URL.
  * Copy the URL to add to your Configuration file.
  * In Slack, in your channel, it will say Added Integration.

NOTE: There is a warning from Slack that this integation is legacy and may be discontinued. if that happens, this script will be updated to accomidate this change.

#### DAPNET (Amateur Radio Operators Only)

The De-Centralized Amateur Paging Network (DAPNET) is a paging network similiar to the old one way messaging paging networks from the 1990's. This is a network for Amateur Radio Operators only, so this section will only pertain to them.

For this to work, you will need to have an account setup with DAPNET to be able to send pages. Configuring the receiving end is up to the user and outside the scope of this setup document.

For this you will need the following:
* DAPNET Username (Typically your callsign)
* DAPNET Password
* The Callsign to send the page to (your callsign probably)
* DAPNET TX-Group - Typically this would be your local regional group for example us-oh

---

### Installing the Script

The next step is installing the needed packages, cloning the repo to get the script and then installing the needed libraries for the script to work properly.

This is probably the easiest step to accomplish.

Please run the following commands on your FreePBX Server:

```bash
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade

sudo apt-get install python3 python3-pip git screen

git clone https://github.com/n8acl/freepbx_call_monitor.git

cd freepbx_call_monitor

pip3 install -r requirements.txt
```
---

## Configure the Script

Now that you have all of your keys/webhooks/what have you, let's configure the script.

You will need to edit the config.py file in the cloned directory. Open this file in your favorite text editor. You should see something similiar:

```python
# Miscellanious Settings
extensions = ['201','202'] # Extensions to Monitor seperated by commas
pbx_mysql_password = 'YOUR FREEPBXUSER MYSQL PASSWORD HERE' # freepbxuser MySQL Password
enable_voicemail_check = True # On = True, Off = False
check_delay = 60 # The amount of time to delay checking the database, in Seconds
voicemail_path = "/var/spool/asterisk/voicemail/default/" # Change this if your voicemail is stored in a different location

# Configure Discord
discord = False # Enable. On = True, Off = False
discord_wh = "YOUR DISCORD WEBHOOK URL HERE"

# Configure Telegram
telegram = False # Enable. On = True, Off = False
telgram_bot_token = 'YOUR TELEGRAM BOT TOKEN HERE'
telegram_chat_id = 'YOUR TELEGRAM CHAT ID HERE'

# Configure Mattermost
mattermost = False # Enable. On = True, Off = False
mattermost_wh_url = 'YOUR MATTERMOST WEBHOOK URL HERE' # This is the part of the URL before the /hook/ part of the Whole URL
mattermost_wh_apikey = 'YOUR MATTERMOST WEBHOOK API KEY HERE' # This is the key that is a mix of letter and numbers after the /hook/ part of the Whole URL

# Configure Slack
slack = False # Enable. On = True, Off = False
slack_wh = 'YOUR SLACK WEBHOOK URL HERE'

# Configure Pushover
pushover = False # Enable. On = True, Off = False
pushover_token = 'YOUR PUSHOVER API KEY TOKEN HERE'
pushover_userkey = 'YOUR PUSHOVER USER KEY HERE'

###################################################
####### This section for Amateur Radio Operators only

# DAPNET configuration
# Note that the username and password below would be the same ones you use to log into the DAPNET Website
dapnet = False # Enable. On = True, Off = False
dapnet_user = "mycall" # Your DAPNET Username, typically your callsign
dapnet_pass = "xxxxxxxxxxxxxxxxxxxx" # Your DAPNET Password
dapnet_send_to = "MYCALL" # The callsign to send the message to for paging
dapnet_txgroup = "us-all" # Your TX-Group. If in the US us-all should work. Otherwise use a more regional tx-group, ex: us-oh

```
At the very top, you will see some settings that are general settings for the script. These variables are:

- ```extenstions``` this is a list of extensions (seperated by commas and each extension enclosed in single quotes) that you want the script to send notifications for. If you have multiple phones on your PBX in a home phone system, for example, you may only want notifications for the extension on your desk. This list allows you to set which extensions notifications are sent for.
- ```pbx_mysql_password``` this is where you paste the key that you got from the freepbx.conf file earlier. Replace where it says YOUR FREEPBXUSER MYSQL PASSWORD HERE, leaving the single quotes around the key.
- ```check_delay``` this is how long of a wait you want the script to check the database. This is set in seconds. Currently, I have mine check it every minute, but you can set this interval to however often you want, however, the longer the interval, the more of a chance you could miss a notification, especailly if you have a busy PBX in the house you are using this on.
- ```enable_voicemail_check``` This turns on or off the check for new voicemails on the system.
- ```voicemail_path``` This is the path to your voicemail folder on your system. This should be pretty standard, but if it's in a different location, you will need to change this to the correct place.

Each section below that contains what is needed for each service to operate. To enable sending to a service, you will need to set the service name from ```False``` to ```True``` and supply the needed keys/webhooks for that service.

---

## Running the Script

Once you have the config file edited, start the bot by typing the following:

```bash
screen -R freepbx_monitor
```

Then in the new window:
```bash
cd freepbx_call_monitor

python3 missedcall.py
```

Once that is done, hold ```CTRL``` and then tap ```A``` and then ```D``` to disconnect from the screen session. If something ever happens, you can reconnect to the session by typing:

```bash
screen -R freepbx_monitor
```

And see why it errored or quit. You will know it errored because it will send the error to whatever server you are using for notifications. This is useful if you need to contact me for support or want to restart the script.

When the script is run, it will send whatever the last call that met the critera to your channel. This is so it can set the last ID for future checks and also to let you know that the script is running.

If you would like the script to run on startup, you can use the supplied ```startbot.sh``` to fire it up on startup. You can either add it to your rc.local file or add it to your crontab to be fired on startup. There are other methods, but all of these are outside the scope of this document.