import datetime

import discord


class ServerPlayersOnlineEmbed(discord.Embed):
    '''Special embed for the players command.'''

    def __init__(self, players=None, lastOnline: int | None = None):
        if players:
            # Create players embed, includes current capacity and player list
            title = f'Players:\t{players.online} / {players.max}'
            description = '-# No players online.'
            if players.sample:
                description = '\n'.join(
                    ['- ' + player.name for player in players.sample])
            # Initialize embed
            super().__init__(title=title, colour=discord.Colour.brand_green(), description=description,
                             footer=discord.EmbedFooter(text='\u200b '), timestamp=datetime.datetime.now(datetime.timezone.utc))
        else:
            super().__init__(description='Server is offline.',
                             colour=discord.Colour.brand_red(), fields=[discord.EmbedField(name='', value=f'-# Last Online: <t:{lastOnline}:R>')])
