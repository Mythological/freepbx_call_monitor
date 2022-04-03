# Miscellanious Settings
extensions = ['201'] # Extensions to Monitor seperated by commas
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