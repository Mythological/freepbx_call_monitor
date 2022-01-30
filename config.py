# Miscellanious Settings
extensions = ['201'] # Extensions to Monitor seperated by commas
pbx_mysql_password = 'YOUR FREEPBXUSER MYSQL PASSWORD HERE' # freepbxuser MySQL Password
check_delay = 60 # The amount of time to delay checking the database, in Seconds

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