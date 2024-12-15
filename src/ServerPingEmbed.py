import datetime

import discord


class ServerPingEmbed(discord.Embed):
    '''Special embed for the ping command.'''

    def __init__(self, ping=None):
        # Create footer
        footer = discord.EmbedFooter(text='\u200b')

        # Create embed depending on if ping is provided, assumes the server is offline if none
        if ping:
            super().__init__(title='Latency', description=f'{ping:.1f} _ms_',
                             colour=discord.Colour.brand_green(), footer=footer, timestamp=datetime.datetime.now(datetime.timezone.utc))
        else:
            super().__init__(title='Latency', description='Server is offline.',
                             colour=discord.Colour.brand_red(), footer=footer, timestamp=datetime.datetime.now(datetime.timezone.utc))
