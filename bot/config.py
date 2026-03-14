#imports
import dotenv
import os
import json

#-Setup-bot---->

#load dotenv
dotenv.load_dotenv()

#Tokens
BOT_TOKEN = os.getenv("BOT_TOKEN")

#Paths
COGS_PATH = "./Cogs"

#-Setup-server--->

#Guilds
GUILDS = [1452248096883867721]

#Roles
MOD_ROLE_ID = 1455553092350120121
MEMBER_ROLE_ID = 1452615315627311114

#-Cogs--->

#Ping
PING_ENABLE = True

#Greeting
#Greetings new members
GREETING_ENABLE = True
GREETING_CHANNEL_ID = 1452256326339264564
GRETTING_MESSAGE = """Nice to see you {name}""" #name = The name of the new member

#Ticket
TICKET_ENABLE = False
TICKET_CATEGORY_NAME = "tickets"
TICKET_CHANNEL_ID = 1452602694404407499
TICKET_MESSAGE = """If you have a question or problem, you can create a ticket to get help."""
#Ticket requests
TICKET_REQUEST_CHANNEL_ID = 1452618589369794743
SHOW_COMPLETED_TICKETS = True

#Rules
RULES_ENABLE = False
RULES_CHANNEL_ID = 1452359057678794752
#Load the rules from JSON
with open("./Rules.json", "r", encoding="UTF-8") as RULES_JSON:
    RULES_JSON = json.load(RULES_JSON)

#Report
REPORT_ENABLE = False
REPORT_CHANNEL_ID = 1457008744171966536

#Voice Channel
#Allows the members to create temporary voice channels and manage them
VOICECHANNEL_ENABLE = True
#The id of the voice channel to create temporary voice channels
VOICE_CHANNEL_ID = 1460662665507635486
#The category under which temporary voice channels will be created.
VOICE_CHANNEL_CATEGORY_ID = 1452248098222116948

#Moderation
#Commands like: /ban, /kick, /timeout
MODERATION_ENABLE = True

#Create Embed
CREATEEMBED_ENABLE = True
CREATEEMBED_CHANNLE_ID = 1479132341644427406
