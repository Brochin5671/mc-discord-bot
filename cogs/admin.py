import discord
from discord.ext import commands
from dotenv import load_dotenv

import os


# Load .env variables
load_dotenv()
ADMIN_ROLE = os.getenv('ADMIN_ROLE')


class Admin(commands.Cog):
    '''Admin commands cog/extension.'''

    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    # Error cases for commands
    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        match error:
            case commands.CommandOnCooldown():
                await ctx.respond(error, ephemeral=True)
            case commands.MissingRole():
                await ctx.respond(error, ephemeral=True)
            case commands.NotOwner():
                await ctx.respond('You must be the owner of this bot to run this command.', ephemeral=True)
            case _:
                raise error

    # Purges a channel's messages.
    @discord.slash_command(name='purge', description='Purges a channel\'s messages.')
    @commands.has_role(ADMIN_ROLE)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def purge(
        self,
        ctx: discord.ApplicationContext,
        limit: discord.Option(
            int, '[Optional] Number of messages to delete.', min_value=1, required=False)  # type: ignore
    ):
        '''Purges a channel\'s messages.'''
        await ctx.defer(ephemeral=True)
        purged = await ctx.channel.purge(limit=limit)
        numPurged = len(purged)
        if numPurged == 1:
            await ctx.respond(f'{len(purged)} message purged.', ephemeral=True)
        else:
            await ctx.respond(f'{len(purged)} messages purged.', ephemeral=True)

    # Reloads the bot's extensions
    @discord.slash_command(name='reload', description='Reloads the bot\'s extensions.')
    @commands.is_owner()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def reload(
        self,
        ctx: discord.ApplicationContext,
    ):
        '''Reloads the bot\'s extensions.'''
        await ctx.defer(ephemeral=True)
        for file in os.listdir('./cogs'):
            if file.endswith('.py') and not file.startswith('_'):
                self.bot.reload_extension(f'cogs.{file[:-3]}')
        await ctx.respond(f'All extensions reloaded.', ephemeral=True)

    # Shutdown the bot
    @discord.slash_command(name='shutdown', description='Shutdown the bot.')
    @commands.is_owner()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def reload(
        self,
        ctx: discord.ApplicationContext,
    ):
        '''Shutdown the bot.'''
        await ctx.respond(f'Goodnight!', ephemeral=True)
        await ctx.bot.close()


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Admin(bot))  # add the cog to the bot
