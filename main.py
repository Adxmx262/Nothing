import interactions
import random

# Settings
SafeMines = '<:robux:1284784245734379551>'
TileMines = '<:bombb:1284784210237980733>'
SafeTowers = '<:starr:1284784911743582248>'
TileTowers = '<:bombb:1284784210237980733>'
BotToken = 'MTA3NTc0OTc5MjQ4NDk2MjM1NA.G7u39C.QoySmAtO_yW7E_lfZ93PqbFMaqEsyy1Buan17M'  # Replace with your actual bot token
AllowedChannelID = 1284808230769266748  # Replace with the actual channel ID where commands can be used

# StartUp
bot = interactions.Client(
    token=BotToken,
    prefix="!",
    intents=interactions.Intents.ALL  # Ensure all necessary intents are enabled
)

# Function to generate Mines grid
def GenGrid(SafeTiles: int):
    BoardNums = random.sample(range(1, 26), SafeTiles)  # Randomly select safe tiles
    Board = [0] * 25
    for Number in BoardNums:
        Board[Number - 1] = 1

    Grid = ""
    endrownums = [6, 11, 16, 21]
    for index, Position in enumerate(Board):
        if (index + 1) in endrownums:
            Grid += f'\n{SafeMines if Position == 1 else TileMines}'
        else:
            Grid += f'{SafeMines if Position == 1 else TileMines}'
    return Grid

# Function to generate Towers grid
def gentower(rows: int):
    if rows > 8:
        return "Max Rows 8!"
    
    row_patterns = [
        f"{SafeTowers}{TileTowers}{TileTowers}",
        f"{TileTowers}{SafeTowers}{TileTowers}",
        f"{TileTowers}{TileTowers}{SafeTowers}"
    ]
    
    return "\n".join(random.choice(row_patterns) for _ in range(rows))

# Command checks
async def check_channel(ctx):
    if ctx.channel.id == AllowedChannelID:
        return True
    else:
        await ctx.send(
            embeds=interactions.Embed(
                title="Invalid Channel",
                description="This command can only be used in the designated channel.",
                color=0xFC4431  # Error color (Red)
            ),
            ephemeral=True
        )
        return False

@bot.command(
    name='mines',
    description="Generates a Mines Grid",
    options=[
        interactions.Option(
            name="clicks",
            description="How many safe spots to generate",
            type=interactions.OptionType.INTEGER,
            required=True,
        )
    ]
)
async def Mines(ctx, clicks: int):
    if ctx.channel.type == interactions.ChannelType.DM:
        await ctx.send(
            embeds=interactions.Embed(
                title="DMs Not Allowed",
                description="This command cannot be used in direct messages.",
                color=0xFC4431  # Error color (Red)
            ),
            ephemeral=True
        )
        return

    if not await check_channel(ctx):
        return

    if int(clicks) > 23:
        await ctx.send(
            embeds=interactions.Embed(
                title="Mines",
                description=f"Too Many Safe Clicks! Max is 23\nYou Chose {clicks}/23",
                color=0xFC4431  # Error color (Red)
            ),
            ephemeral=True
        )
        return

    try:
        mines = interactions.Embed(
            title="-Spectral Predictor-",
            description="!WARNING! This is not 100% prediction.",
            color=0xFFFFFF  # Success color (White)
        )
        mines.add_field(name=f"Field {clicks} Clicks", value=GenGrid(clicks), inline=True)
        await ctx.send(embeds=mines, ephemeral=True)
    except Exception as e:
        await ctx.send(
            embeds=interactions.Embed(
                title="Mines",
                description="Error generating grid!",
                color=0xFC4431  # Error color (Red)
            ),
            ephemeral=True
        )
        print(f"Error in Mines command: {e}")

@bot.command(
    name='towers',
    description="Generates a Tower Grid",
    options=[
        interactions.Option(
            name="rows",
            description="How many rows to generate",
            type=interactions.OptionType.INTEGER,
            required=True,
        )
    ]
)
async def Towers(ctx, rows: int):
    if ctx.channel.type == interactions.ChannelType.DM:
        await ctx.send(
            embeds=interactions.Embed(
                title="DMs Not Allowed",
                description="This command cannot be used in direct messages.",
                color=0xFC4431  # Error color (Red)
            ),
            ephemeral=True
        )
        return

    if not await check_channel(ctx):
        return

    if int(rows) > 8:
        await ctx.send(
            embeds=interactions.Embed(
                title="Towers",
                description=f"Too Many Rows! Max is 8\nYou Chose {rows}/8",
                color=0xFC4431  # Error color (Red)
            ),
            ephemeral=True
        )
        return

    try:
        towers = interactions.Embed(
            title="Towers",
            description="Generated Tower!",
            color=0xFFFFFF  # Success color (White)
        )
        towers.add_field(name=f"Field {rows} Rows", value=gentower(rows), inline=True)
        await ctx.send(embeds=towers, ephemeral=True)
    except Exception as e:
        await ctx.send(
            embeds=interactions.Embed(
                title="Towers",
                description="Error generating tower!",
                color=0xFC4431  # Error color (Red)
            ),
            ephemeral=True
        )
        print(f"Error in Towers command: {e}")

# Start the bot
bot.start()
