#############################
# Import Libraries
import config as cfg
import subprocess
from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed

#############################
# Define Variables

linefeed = "\r\n"
call_log = []
last_id = ''

#############################
# Define Functions

def send_discord (title, msg):
    webhook = DiscordWebhook(url=cfg.discord_wh["pbx"])

    embed = DiscordEmbed(title=title, description=msg)
    webhook.add_embed(embed)

    response = webhook.execute() 

#############################
# Main Program

try:
    while True:
        cmd = """
        echo "SELECT 
        date_format(calldate,'%m/%d/%Y %H:%i') AS Timestamp, 
        clid AS Caller, 
        disposition AS Status, 
        lastapp AS LastApp,
        uniqueid as ID 
        from cdr 
        where disposition = 'NO ANSWER'
        or disposition = 'BUSY'
        ORDER BY calldate DESC
        limit 1"  | mysql -u freepbxuser -p"""

        cmd = cmd + cfg.pbx_mysql_password

        cmd = cmd + """ -sN asteriskcdrdb"""

        call_log = subprocess.check_output(cmd, shell=True, universal_newlines=True).replace('\t',',').split(',')

        if last_id != call_log[4]:
            message = "TimeStamp: " + call_log[0] + linefeed
            message = message + "Caller: " + call_log[1] + linefeed
            message = message + "Status: " + call_log[2] + linefeed
            # message = message + "Last App: " + call_log[3]

            last_id = call_log[4]

            send_discord('Missed Call', message)

        sleep(cfg.check_delay)
except KeyboardInterrupt:
    send_discord("Error Message","FreePBX Monitor has been stopped. KeyboardInterrupt")

except Exception as e:
    send_discord("Error Message",str(e))
