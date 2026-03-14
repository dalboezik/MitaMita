# MitaMita a discord utility bot
Modular Discord server management bot built with Python and disnake.
The bot provides multiple server utilities such as moderation commands, greeting new members, temporary voice channels, embed creation tools, and more.

The project is organized using a Cog-based architecture, making it easy to expand and maintain.

---

# Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)

---

# Features
## Moderation
- Slash commands for moderation acrions:
    - Ban users
    - Kick users
    - Timeout users

## Greeting System
- Automatically greets new members when they join.
    - Sends customizable welcome messages.

## Temporary Voice Channels
- Members can create temporary voice channels.
- Channel owner can:
    - Rename the channel
    - Set user limit

## Ticket System
- Users can create support tickets.
- Tickets are created in a dedicated category.
- Optional display of completed ticket.

## Rule System
- Automatically sends server rules from a JSON file.

## Reporting System
- Members can report users to moderators.

## Embed Creator
- Interactive embed builder for creating rich Discord messages.
- Supports:
    - Custom title
    - Fields
    - Images

## Ping Command
- Basic command to test if the bot is online.

---

# Project Structure
```
bot/
│
├── main.py                # Entry point for the bot
├── bot_init.py            # Bot initialization
├── config.py              # Configuration and feature toggles
│
├── Cogs/                  # Feature modules
│   ├── Ping.py
│   ├── Greeting.py
│   ├── Moderation.py
│   ├── Ticket.py
│   ├── Rules.py
│   ├── CreateEmbed.py
│   └── VoiceChannel.py
│
├── Modals/                # Discord modal interactions
│   ├── Moderation/
│   ├── CreateEmbed/
│   ├── Voicechannel/
│   └── ticket_modal.py
│
├── SelectMenus/           # Dropdown UI components
│   └── CreateEmbed/
│
├── utils/
│   ├── load_cogs.py       # Automatically loads all cogs
│   └── delete_chat_history.py
│
├── Rules.json             # Server rules configuration
└── .env                   # Environment variables
```

---

# Installation
Clone the reposetory 

# Configuration
## 1. Create a ``.env`` file
    BOT_TOKEN=your_discord_bot_token
## 2. Configure ``config.py``
Edit the configuration file to match your server:

**Example:**
```
PING_ENABLE = True
GREETING_ENABLE = True
TICKET_ENABLE = False
VOICECHANNEL_ENABLE = True
MODERATION_ENABLE = True
CREATEEMBED_ENABLE = True
```

**You can also configure:**

- Channel IDs
- Role IDs
- Ticket categories
- Rule display
- Greeting messages

**Example greeting:**
GRETTING_MESSAGE = "Nice to see you {name}"

---

# Usage
Start the bot:
    ``python main.py``

When the bor starts it will:
1. Connect to discord
2. Load all selected cogs
3. Initialize enabled systems (rules, ticket panel, embed builder)

Console output:
    ``BotName#1234 is online!``

---

# Dependencies
Main libaries used:
- disnake - Discord API wrapper
- dotenv - Enviroment variable management
- Python 3.10+

Install them with:
    ``pip install disnake dotenv``

---

# Troubleshooting
**Bot does not start** <br>
check:
- ``.env`` exists
- ``BOT_TOKEN`` is correct
- python version is compatible

**Slash commands not appearing** <br>
Try syncing commands or reinviting the bot with the correct scopes: <br>

    applications.commands
    bot

**Cog not loading**
Verify that:
- The cog file exists inside ``/Cogs``
- The feature is enabled in ``config.py``
