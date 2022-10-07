# Mantra Bot

This is the planlist of all the tasks to be completed in the v1 of the Mantra bot!

## Libraries that can be used

- [x] hikari-py
- [ ] disnake
- [ ] py-cord
- [ ] discord.js

# Installation

First of all check `.env.example` for Examples on environment variables.

Clone the repository using

```bash
git clone https://github.com/Mantra-Development/Mantra-Bot
cd Mantra-Bot
poetry shell
poetry install
python -m mantra
```

## With Docker

```bash
git clone https://github.com/Mantra-Development/Mantra-Bot
cd Mantra-Bot
docker-compose build
docker-compose up
```

You're up and running!

# Commands that can be implemented

### Owner Commands

| Command      | Description                        | Command Type  | Checklist |
| ------------ | ---------------------------------- | ------------- | --------- |
| eval         | Run Python code in bot environment | Modals        |           |
| (re/un) load | Reload/Unload/Load Plugins         | Slash Command |           |

### General System Commands

| Command                | Description             | Command Type  | Checklist |
| ---------------------- | ----------------------- | ------------- | --------- |
| info                   | Some info about the bot | Slash Command |           |
| ping                   | Ping of the Bot         | Slash Command |           |
| userinfo               | Info of a user          | User Command  |           |
| serverinfo             | Info of a server        | Slash Command |           |
| emoji                  | Emoji Commands          | Slash Command |           |
| steal                  | Steal Emoji             | Slash Command |           |
| Android Clyde Commands | Self Explanatory        | Slash Command |           |
| tag                    | Tags Command            | Slash Command |           |

### Fun Commands

| Command    | Description                  | Command Type  | Checklist |
| ---------- | ---------------------------- | ------------- | --------- |
| 8ball      | Magic 8Ball                  | Slash Command |           |
| urban      | Get words meaning from Urban | Slash Command |           |
| google     | Google a word                | Slash Command |           |
| duckduckgo | Ddg a word                   | Slash Command |           |
| reverse    | Reverse a given Text         | Slash Command |           |
| coin       | Flip a coin                  | Slash Command |           |
| dog        | Dog image and fact           | Slash Command |           |
| cat        | Cat image and fact           | Slash Command |           |
| bird       | Bird image and fact          | Slash Command |           |
| memes      | Get memes                    | Slash Command |           |

### Utilities Commands

| Command         | Description                      | Command Type    | Checklist |
| --------------- | -------------------------------- | --------------- | --------- |
| embed           | Embed Builder using buttons      | Slash Command   |           |
| say             | Say command to make the bot talk | Slash Command   |           |
| translate       | Self Explanatory                 | Message Command |           |
| Leveling System | Self Explanatory                 | Slash Command   |           |
| remainder       | Remind you of things             | Slash Command   |           |
| starboard       | Star messages (Togglable)        | Slash Command   |           |

### Moderation Commands

| Command  | Description                                  | Permissions     | Command Type  | Checklist |
| -------- | -------------------------------------------- | --------------- | ------------- | --------- |
| timeout  | (Un)-Timeout a member                        | Manage Messages | Slash Command |           |
| kick     | Kick a member                                | Kick Members    | Slash Command |           |
| ban      | Ban a member(Also Include Temp-Ban)          | Ban Members     | Slash Command |           |
| purge    | Purge messages                               | Manage Messages | Slash Command |           |
| role     | Role commands(Add/Remove)                    | Manage Roles    | Slash Command |           |
| slowmode | Enable/Disable Slowmode                      | Manage Channel  | Slash Command |           |
| warn     | Warning Related Commands                     | Manage Messages | Slash Command |           |
| case     | Inflict a case with every moderation command | Manage Messages | Slash Command |           |
