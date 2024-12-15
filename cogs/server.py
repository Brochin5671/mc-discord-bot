import datetime
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from mcstatus import JavaServer

import os

from src import ServerStatusEmbed, ServerPingEmbed, ServerPlayersOnlineEmbed, get_value_from_json, write_value_to_json

# Load .env variables
load_dotenv()
STATUS_CHANNEL_ID = int(os.getenv('STATUS_CHANNEL_ID'))
MC_SERVER_IP = os.getenv('MC_SERVER_IP')
DATA_PATH = os.getenv('DATA_PATH')


class Server(commands.Cog):
    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot
        # Different values to indicate startup of bot
        self.playersOnline = ''
        self.isOnline = None
        # Read lastOnline timestamp from cache if exists
        self.lastOnline = get_value_from_json(
            f'{DATA_PATH}cache.json', 'lastOnline')
        # Start task
        self.server_status_task.start()

    # Stop running task if cog/extension is unloaded
    def cog_unload(self):
        self.server_status_task.cancel()

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(error, ephemeral=True)
        else:
            raise error

    # Constantly get the status of the Minecraft server
    @tasks.loop(reconnect=True)
    async def server_status_task(self):
        try:
            # Get server and status
            server = await JavaServer.async_lookup(MC_SERVER_IP)
            status = await server.async_status()
            # Write current datetime timestamp to cache and keep it
            self.lastOnline = int(datetime.datetime.now(
                datetime.timezone.utc).timestamp())
            write_value_to_json(f'{DATA_PATH}cache.json',
                                'lastOnline', self.lastOnline)
            # Create markdown list of players if not empty
            players = status.players.sample
            if players:
                playersOnline = '\n'.join(
                    ['- ' + player.name for player in players])
            else:
                playersOnline = None
            # Send status if player list has changed or previous state of server was offline
            if playersOnline != self.playersOnline or not self.isOnline:
                # Update values
                self.isOnline = True
                self.playersOnline = playersOnline
                # Send status to channel
                channel = self.bot.get_channel(STATUS_CHANNEL_ID)
                await channel.send(embed=ServerStatusEmbed(status))
        except (ConnectionResetError, TimeoutError) as e:
            # Send offline status if previous state was online or bot just started up
            if self.isOnline or self.isOnline is None:
                self.isOnline = False
                channel = self.bot.get_channel(STATUS_CHANNEL_ID)
                await channel.send(embed=ServerStatusEmbed(lastOnline=self.lastOnline))
        except Exception as e:
            print(e)

    # Wait until bot is ready
    @server_status_task.before_loop
    async def before_server_status_task(self):
        await self.bot.wait_until_ready()

    # Create command group
    serverGroup = discord.SlashCommandGroup(
        "server", "Anything to do with the Minecraft server")

    # Displays the server's general stats
    @serverGroup.command(name='status', description='Displays the server\'s general stats.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def server_status(self, ctx: discord.ApplicationContext):
        '''Displays the server\'s general stats.'''
        try:
            # Defer and wait to get status
            await ctx.defer(ephemeral=True)
            server = await JavaServer.async_lookup(MC_SERVER_IP)
            status = await server.async_status()
            await ctx.respond(embed=ServerStatusEmbed(data=status), ephemeral=True)
        except (ConnectionResetError, TimeoutError):
            await ctx.respond(embed=ServerStatusEmbed(lastOnline=self.lastOnline), ephemeral=True)
        except Exception as e:
            print(e)

    # Displays the server's latency to the bot
    @serverGroup.command(name='ping', description='Displays the server\'s latency to the bot.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def server_latency(self, ctx: discord.ApplicationContext):
        '''Displays the server\'s latency to the bot.'''
        try:
            # Defer and wait to get ping
            await ctx.defer(ephemeral=True)
            server = await JavaServer.async_lookup(MC_SERVER_IP)
            ping = await server.async_ping()
            await ctx.respond(embed=ServerPingEmbed(ping), ephemeral=True)
        except (ConnectionResetError, TimeoutError):
            await ctx.respond(embed=ServerPingEmbed(), ephemeral=True)
        except Exception as e:
            print(e)

    # Displays who's currently online
    @serverGroup.command(name='players', description='Displays who\'s currently online.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def server_players_online(self, ctx: discord.ApplicationContext):
        '''Displays who\'s currently online.'''
        try:
            # Defer and wait to get status
            await ctx.defer(ephemeral=True)
            server = await JavaServer.async_lookup(MC_SERVER_IP)
            status = await server.async_status()
            await ctx.respond(embed=ServerPlayersOnlineEmbed(status.players), ephemeral=True)
        except (ConnectionResetError, TimeoutError):
            await ctx.respond(embed=ServerPlayersOnlineEmbed(lastOnline=self.lastOnline), ephemeral=True)
        except Exception as e:
            print(e)


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Server(bot))  # add the cog to the bot
