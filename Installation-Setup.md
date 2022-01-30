### Installation Steps
1) [Obtain MySQL Password for freepbxuser from MySQL](Installation-Setup.md#get-freepbxuser-mysql-password)
2) Obtain API Keys/Webhook URL 
3) Install needed packages, clone Repo and install library dependencies
4) Configure the script
5) Run the Script

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

### Messaging Service

Here we need to setup the service you want to get the notifications from.

#### Discord Webhook URL

If you will be using Discord, you will need to configure your Discord server.

- Create a new text channel for the bot (I called mine #pbx-alerts).
- Go to the settings of your server and click on integrations (right click the server icon and go to server settings and then integrations).
- In the middle of the screen should be a button that says "Create Webhook". Click that.
- Give it a name (I used FreePBX for mine) and select the new text channel you just created, or use an existing channel if you like.
- Click the "Copy Webhook URL" button at the bottom of the window. Paste this somewhere as you will need it here shortly again. (If loose it, you can come back later after creation and click the Copy button again).
- Click "Save". Your Webhook and Channel are ready.

##### Telegram

If using Telegram, note that any bot you have will work. For example, if you have a bot that you already use for your home automations, you could use that bot for this as well. I created a seperate bot from my home automation bot for APRS/Ham Radio use, but I could have just as easily used my home automation bot.

* If you plan on using Telegram:
    - You will need to first either create a Telegram bot or use an existing one you own. If this is your first bot, you can use the [steps here](https://core.telegram.org/bots#6-botfather) and talk to @BotFather to create your bot. You will need the bot token for the bot you are using/creating and this can also be obtained from talking to @BotFather.
    - You will also need your chatid. This can be obtained once your bot is up and running by sending a message to your bot and using the Telegram API by going to this url: [https://api.telegram.org/bot'API-access-token'/getUpdates?offset=0](https://api.telegram.org/bot<API-access-token>/getUpdates?offset=0) replacing 'API-access-token' with your bot access token you obtained in the previous step. You will see some json and you will be able to find your ID there in the From stanza.
    - Note that Influx DB provides some examples of what to look for in the above 2 steps. You can go to their page by [clicking here](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/).
    - NOTE: Telegram is required for APRS message notification to work.

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

## Configure the Script

Now that you have your MySQL Password and your Discord Webhook, let's configure the script.

You will need to edit the config.py file in the cloned directory. Open this file in your favorite text editor. You should see something similiar:

```python
pbx_mysql_password = 'MYSQL FREEPBXUSER PASSWORD HERE'

discord_wh = {
    "pbx": "YOUR DISCORD WEBHOOK HERE"
}

check_delay = 60 # This is the amount of time to delay checks to the database. Set in Seconds
```

- ```pbx_mysql_password``` this is where you paste the key that you got from the freepbx.conf file earlier. Replace where it says MYSQL FREEPBXUSER PASSWORD HERE, leaving the single quotes around the key.
- ```discord_wh``` this is where you need to paste that Webhook URL you got from Discord earlier. Replace where it says YOUR DISCORD WEBHOOK HERE, again leaving the quotes around it.
- ```check_delay``` this is how long of a wait you want the script to check the database. This is set in seconds. Currently, I have mine check it every minute, but you can set this interval to however often you want, however, the longer the interval, the more of a chance you could miss a notification, especailly if you have a busy PBX in the house you are using this on.

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

And see why it errored or quit. You will know it errored because it will send the error to the Discord Channel. This is useful if you need to contact me for support or want to restart the script.

When the script is run, it will send whatever the last call that met the critera to your channel. This is so it can set the last ID for future checks and also to let you know that the script is running.

