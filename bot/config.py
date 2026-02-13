#imports
import dotenv
import os
import json

#load dotenv
dotenv.load_dotenv()

#Tokens
BOT_TOKEN = os.getenv("BOT_TOKEN")

#Paths
COGS_PATH = "./Cogs"

#Roles
MOD_ROLE_ID = 1455553092350120121
MEMBER_ROLE_ID = 1452615315627311114

#Cogs --->

#Ping
PING_ENABLE = True

#Greeting
#Neue Mitglieder mit einem Embed grüßen
GREETING_ENABLE = True
GREETING_CHANNEL_ID = 1452256326339264564
GRETTING_MESSAGE = """Schön, dass du da bist {name}""" #name = Name von dem Member, der beigetrtten ist

#Ticket
TICKET_ENABLE = False
TICKET_CATEGORY_NAME = "tickets"
TICKET_CHANNEL_ID = 1452602694404407499
TICKET_MESSAGE = """Wenn du eine Frage oder ein Problem hast, kannst du einen Ticket erstellen."""
#Ticket requests
TICKET_REQUEST_CHANNEL_ID = 1452618589369794743
SHOW_COMPLETED_TICKETS = True

#Rules
RULES_ENABLE = False
RULES_CHANNEL_ID = 1452359057678794752
with open("./Rules.json", "r", encoding="UTF-8") as RULES_JSON:
    RULES_JSON = json.load(RULES_JSON)

#Report
REPORT_ENABLE = False
REPORT_CHANNEL_ID = 1457008744171966536

#Voice Channel
#Ermöglicht den Mitgliedern, eigene temporäre Voicechannels zu erstellen und die zu verwalten
VOICECHANNEL_ENABLE = True
VOICE_CHANNEL_ID = 1460662665507635486 #Voicechannel, mit dem die Mitglieder eigene Voicechannels erstellen können
VOICE_CHANNEL_CATEGORY_ID = 1452248098222116948 #Kategorie für die Voicechannels von den Mitgliedern

#Moderation
#Commands, wie: /ban, /kick, /timeout
MODERATION_ENABLE = True

#Create Embed
CREATEEMBED_ENABLE = True
