import datetime

import discord


class ServerStatusEmbed(discord.Embed):
    '''Special embed for the status command.'''

    def __init__(self, data=None, lastOnline: datetime.datetime | None = None):
        # Create embed depending on if data is provided, assumes the server is offline if none
        if data:
            fields = []

            # Create players field, includes current capacity and player list
            players = data.players
            playersFieldName = f'Players:\t{players.online} / {players.max}'
            playersFieldValue = '-# No players online.'
            if players.sample:
                playersFieldValue = '\n'.join(
                    ['- ' + player.name for player in players.sample])
            fields.append(discord.EmbedField(
                name=playersFieldName, value=playersFieldValue))
            # Create version field, includes game and protocol version
            version = data.version.name
            protocolVersion = data.version.protocol
            fields.append(discord.EmbedField(name='Version',
                          value=f'{version} ({protocolVersion})'))
            # Create latency field
            latency = data.latency
            fields.append(discord.EmbedField(
                name='Latency', value=f'{latency:.1f} _ms_'))
            # Initialize embed
            super().__init__(title='Server Status', description='Online',
                             colour=discord.Colour.brand_green(), fields=fields, footer=discord.EmbedFooter(text='\u200b '), timestamp=datetime.datetime.now(datetime.timezone.utc))
        else:
            super().__init__(title='Server Status', description='Offline',
                             colour=discord.Colour.brand_red(), fields=[discord.EmbedField(name='', value=f'-# Last Online: <t:{lastOnline}:R>')])
