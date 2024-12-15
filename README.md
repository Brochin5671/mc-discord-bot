# Minecraft Server Discord Bot

**By Maxim Brochin**

A simple Python program to deploy your Discord bot for your Minecraft **Java** server on your Discord server(s). Has the ability to display the state of the server alongside other information using the package _[mcstatus](https://pypi.org/project/mcstatus/)_. Can also perform operations in Discord servers like purging messages.

Why I built this, see [Why?](#Why?)

More features are planned, see [Planned Features](#Planned-Features)

## Usage

### Commands

**These are all slash commands, prefixed with a `/`.**

#### Owner

- `reload`: Reloads the bot's cogs/extensions in the `./cogs` directory
- `shutdown`: Closes the bot's connection to Discord

#### Admin

- `purge`: Purges a channel's messages, optional `limit` parameter

#### User

##### Minecraft Server Commands

- `server status`: Displays the current state of the server alongside player count, player list, game and protocol version, and latency to bot. If the server is offline, it will use a saved value, displaying how long ago the server was previously online
- `server ping`: Displays the server's latency between the bot
- `server players`: Displays a list of players currently online

### Tasks

- **Status:** same as the command `server status`, displays the current state of the server alongside player count, player list, game and protocol version, and latency to bot. If the server is offline, it will use a saved value, displaying how long ago the server was previously online. **The bot must be provided a channel to post status updates about the server.**

## Prerequisites

Ensure your app is created and configured using the [Discord Developer Portal](https://discord.com/developers/docs/quick-start/getting-started#step-1-creating-an-app).
**NOTE: You just need your bot token when following the instructions.**

Find `server.properties` in the root directory of your Minecraft server folder. Ensure `enable-status` is set to `true`.

```bash
...
enable-status=true
...
```

Ensure that you are at least using **Python v3.11** and a Linux environment for the bot.

## Setup

**This assumes you are using a Linux environment.**

Clone the repository.

```bash
git clone "https://github.com/Brochin5671/mc-discord-bot.git" && cd "mc-discord-bot"
```

Install _virtualenv_ if you haven't already.

```bash
pip install virtualenv
```

Create a virtual environment.

```bash
python<version> -m venv venv
```

Activate it.

```bash
source env/bin/activate
```

Use the package manager _[pip](https://pip.pypa.io/en/stable/)_ to install requirements.

```bash
pip install -r requirements.txt
```

Create and configure your `.env` file.

```bash
# This will be the secret key for connecting to your bot
BOT_TOKEN=""
# The Minecraft Java Server's IP
MC_SERVER_IP=""
# A list of server IDs in the format "<id1>,<id2>, ..." or just one ID that your bot will be in
GUILD_IDS=""
# The channel ID where the bot will post the Minecraft server's status
STATUS_CHANNEL_ID=""
# Name of the admin role to use certain slash commands
ADMIN_ROLE=""
# Path to the directory containing any bot-created files, leave empty if using the root directory
DATA_PATH=""
```

## Why?

I wanted to expand on my Python understanding, reinforcing and learning concepts, building a system, and exploring what's possible. I was also killing some time by playing Minecraft: Java Edition with friends, so I thought this would be a great opportunity to demonstrate my skills and have others use the bot I built.

## Planned Features

### Commands

- `server sysinfo`: Display the server's system information like CPU and memory usage
- `sync`: Syncs the user's account with the given player in Minecraft (this will be used for stats and other operation later)
- `player stats`: Display any player stats of the given player or user's. An optional `<player_name>` or `<discord
_name>` argument can be provided

### Ideas

- More server commands and interactions (like an API to run certain commands securely without using RCON)
- Fun ways of having used the sync feature like a measure of wealth based on the resources the player has

### Improvements

- Refactor code
- Discover performance bottlenecks and **squash** them

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
