#################################################################################

# FreePBX Missed Call Monitor
# Developed by: Jeff Lehman, N8ACL
# Current Version: 04022022
# https://github.com/n8acl/freepbx-call-monitor

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@qsl.net
# Twitter: @n8acl
# Discord: Ravendos#7364
# Mastodon: @n8acl@mastodon.radio
# Website: https://www.qsl.net/n8acl

###################   DO NOT CHANGE BELOW   #########################

#############################
# Import Libraries
import glob
import os
import config as cfg
import subprocess
import http.client, urllib
import json
import requests
from requests.auth import HTTPBasicAuth
from time import sleep

if cfg.telegram:
    try: 
        import telegram
    except ImportError:
        exit('This script requires the python-telegram-bot module\nInstall with: pip3 install python-telegram-bot')

if cfg.discord:
    try:
        from discord_webhook import DiscordWebhook, DiscordEmbed
    except ImportError:
        exit('This script requires the discord_webhook module\nInstall with: pip3 install discord_webhook')

if cfg.mattermost:
    try:
        from matterhook import Webhook
    except ImportError:
        exit('This script requires the matterhook module\nInstall with: pip3 install matterhook')

#############################
# Define Variables
linefeed = "\r\n"
dapnet_url = 'http://www.hampager.de:8080/calls' # API URL, DO NOT CHANGE
call_log = []
last_id = ''
message = ''
dapnet_message = ''
latest_voicemail = []
voicemail_path = cfg.voicemail_path

#############################
# Define Functions

def send_telegram(msg, bot_token, chat_id):
    # Create Telegram Object
    bot = telegram.Bot(token=bot_token)

    # Send message to Telegram
    bot.sendMessage(chat_id=chat_id, text=msg)

def send_discord(msg,wh_url, title, send_as_embed):
    # Check to send as either an embed or as a regular Text Message
    if send_as_embed:
        webhook = DiscordWebhook(url=wh_url)

        embed = DiscordEmbed(title=title, description=msg)
        webhook.add_embed(embed)
    else:
        webhook = DiscordWebhook(url=wh_url, content=msg)

    # Send Message to Discord
    response = webhook.execute() 

def send_mattermost(msg,wh_url, api_key):
    # Create Bot Object
    mm_bot = Webhook(mattermostwh["wh_url"], mattermostwh["apikey"])
    
    # Send to Mattermost
    mm_bot.send(msg)  

def send_pushover(msg, pushover_token, pushover_userkey):
    # Send to Pushover
    connn = http.client.HTTPSConnection("api.pushover.net:443")
    connn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
        "token": pushover_token,
        "user": pushover_userkey,
        "message": msg,
        }), { "Content-type": "application/x-www-form-urlencoded" })
    connn.getresponse()

def send_slack(msg, wh_url):
 
    response = requests.post(
        wh_url, data=json.dumps(msg),
        headers={'Content-Type': 'application/json'}
    )

def send_dapnet(text):

    data = json.dumps({"text": text, "callSignNames": [cfg.dapnet_send_to], "transmitterGroupNames": [cfg.dapnet_txgroup], "emergency": False})
    response = requests.post(dapnet_url, data=data, auth=HTTPBasicAuth(cfg.dapnet_user,cfg.dapnet_pass)) 



#############################
# Main Program

try:
    while True:
        ####### Check for missed Call
        cmd = """
        echo "SELECT 
        date_format(calldate,'%m/%d/%Y %H:%i') AS Timestamp, 
        clid AS Caller, 
        disposition AS Status, 
        lastapp AS LastApp,
        uniqueid as ID 
        from cdr 
        where dstchannel like '%"""
        for x in range(0,len(cfg.extensions)):
            cmd = cmd + cfg.extensions[x] + "%'"
            if x < len(cfg.extensions)-1:
                cmd = cmd + " or dstchannel like '%"
            else:
                break

        cmd = cmd + """

        ORDER BY calldate DESC
        limit 1"  | mysql -u freepbxuser -p"""

        cmd = cmd + cfg.pbx_mysql_password

        cmd = cmd + """ -sN asteriskcdrdb"""

        call_log = subprocess.check_output(cmd, shell=True, universal_newlines=True).replace('\t',',').split(',')

        if last_id != call_log[4]:
            if call_log[2] == 'NO ANSWER':
                message = "TimeStamp: " + call_log[0] + linefeed
                message = message + "Caller: " + call_log[1] + linefeed
                message = message + "Status: " + call_log[2] + linefeed
                dapnet_message = "Missed Call From: " + call_log[1]

            elif call_log[2] == 'ANSWERED' and call_log[3] == 'VOICEMAIL':
                message = "TimeStamp: " + call_log[0] + linefeed
                message = message + "Caller: " + call_log[1] + linefeed
                message = message + "Status: " + call_log[2] + " by " + call_log[3] + linefeed
                dapnet_message = "Missed Call from: " + call_log[1]

            else:
                message = ''
                dapnet_messsage = ''

            last_id = call_log[4]
            
            if message != '':
                if cfg.discord:
                    send_discord(message, cfg.discord_wh, 'Missed Call', True)
                if cfg.telegram:
                    send_telegram(message, cfg.telegram_bot_token, cfg.telegram_chat_id)
                if cfg.slack:
                    slack_msg = {'text': message}
                    send_slack(msg, cfg.slack_wh)
                if cfg.mattermost:
                    send_mattermost(message, cfg.mattermost_wh_url, cfg.mattermost_wh_apikey)
                if cfg.pushover:
                    send_pushover(message, cfg.pushover_token, cfg.pushover_userkey)
                if cfg.dapnet:
                    send_dapnet(dapnet_message)
        message = ''
        dapnet_message = ''

        #### Check for new Voicemail
        for x in range(0,len(cfg.extensions)):
            list_of_files = glob.glob(voicemail_path + cfg.extensions[x] + "/INBOX/*.txt")
            if len(list_of_files) == 0:
                latest_voicemail.clear()
            else:
                latest_file = max(list_of_files, key=os.path.getctime)
                if cfg.extensions[x] + ' - ' + latest_file not in latest_voicemail:
                    with open(latest_file,'r') as f:
                        for line in f:
                            if 'origmailbox' in line:
                                on_extension = line[12:len(line)]
                            if 'callerid' in line:
                                callerid = line[9:len(line)]
                            if 'origdate' in line:
                                vm_timestamp = line[13:len(line)]
                            if 'duration' in line:
                                duration = line[9:len(line)]
                    
                    message = "TimeStamp: " + vm_timestamp
                    message = message + "Caller: " + callerid
                    message = message + "Duration (sec): " + duration + linefeed
                    message = message + "Total number of VM's on extension: " + str(len(list_of_files))
                    dapnet_message = "New Voicemail from: " + callerid

                if message != '':
                    if cfg.discord:
                        send_discord(message, cfg.discord_wh, 'New Voicemail on ' + on_extension, True)
                    if cfg.telegram:
                        send_telegram('New Voicemail: ' + message, cfg.telegram_bot_token, cfg.telegram_chat_id)
                    if cfg.slack:
                        slack_msg = {'text': 'New Voicemail: ' + message}
                        send_slack(msg, cfg.slack_wh)
                    if cfg.mattermost:
                        send_mattermost('New Voicemail: ' + message, cfg.mattermost_wh_url, cfg.mattermost_wh_apikey)
                    if cfg.pushover:
                        send_pushover('New Voicemail: ' + message, cfg.pushover_token, cfg.pushover_userkey)
                    if cfg.dapnet:
                        send_dapnet(dapnet_message)

                    latest_voicemail.append(cfg.extensions[x] + ' - ' + latest_file)
        message = ''
        dapnet_message = ''

        sleep(cfg.check_delay)
# except KeyboardInterrupt:
#     send_discord("FreePBX Monitor has been stopped. KeyboardInterrupt", cfg.discord_wh, "Error Message",True)

except Exception as e:
    send_discord(str(e), cfg.discord_wh, "Error Message",True)
