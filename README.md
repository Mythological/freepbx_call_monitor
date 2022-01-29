# FreePBX Missed Call Monitor
Python based notifications of missed calls to FreePBX/Asterisk in Discord

---

# Description

This is a Python based script that will pull the last missed call data from the asteriskcdrdb database table on a FreePBX Server and send a notification with the missed call information parsed to Discord.

I wanted an easy way to get notifications of a missed call coming into my home PBX when I was away from home. I also use my PBX for the Hamshack Hotline, a VOIP Phone based system strictly for Amateur Radio Operators, so I needed a way to get notification of a missed call.

Note that this is not solely for the use of Amateur Radio Operators, but for anyone who wants to get missed call notifications to their own Discord Server.

## Assumptions

For this script, the following is assumed

- You have an already configured FreePBX/Asterisk Server.
  - This has been run and tested on a server that has Ubuntu 20.02 Server installed and Incredible PBX installed on it.
  - If you can install Python3 on the FreePBX Server, you should be able to run this.

- You have a Discord Server that you are able to administrate
  - I have one that I use for my network and other notifications and also as a family server.

---

## FreePBX/Asterisk Versions

Currently, this works with the following PBX Version:

|Software|Version|
|--------|-------|
|Incredible PBX|2021.01U for Ubuntu 20.04|
|FreePBX|15.0.17.55|
|Asterisk|18.6.0|

You may need to tweak the sql query to make sure it is pulling from the correct database, but this should not change often. As my PBX is updated, I will test and update this script of course.

---

# Installation/Setup

### Installation Steps
1) Obtain Webhook URL and MySQL Password
2) Install needed packages, clone Repo and install library dependencies
3) Configure the script

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

### Discord Webhook URL

Now you will need to configure your Discord server.

- Create a new text channel for the bot (I called mine #pbx-alerts).
- Go to the settings of your server and click on integrations (right click the server icon and go to server settings and then integrations).
- In the middle of the screen should be a button that says "Create Webhook". Click that.
- Give it a name (I used FreePBX for mine) and select the new text channel you just created, or use an existing channel if you like.
- Click the "Copy Webhook URL" button at the bottom of the window. Paste this somewhere as you will need it here shortly again. (If loose it, you can come back later after creation and click the Copy button again).
- Click "Save". Your Webhook and Channel are ready.

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

---

## Contact
If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Twitter: @n8acl
- Discord: Ravendos#7364
- Mastodon: @n8acl@mastodon.radio
- E-mail: n8acl@qsl.net

Or open an issue on Github. I will respond to it, and of course you, when I can. 

If you reach out to me and have an error, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. Otherwise just reach out to me :).

---

## Change Log

* 01/29/2022 - Inital Release
