import discord
from discord.ext import commands
from datetime import datetime

# T String
token_string = "OTM3NDQ3MjkyNjE1NjU1NTM2.Yfb30w.QqD4gPsCAfiz0nDN_uFdL9zjRW8"

bot = commands.Bot(command_prefix="$")

# # Game Variables
# game = ""
# time = ""
# time_zone = ""
# opponent = ""
# streamable = ""

# The connection to discord
client = discord.Client()


# Decorator as an event
# on_ready runs when bot is first set up
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_raw_reaction_add(reaction):
    msg = reaction
    print(reaction.message_id)


# Function runs when message is sent
@client.event
async def on_message(message):
    # Set what channel we are in
    channel = message.channel

    if message.author == client.user:
        return

    if message.content.startswith("$new"):
        print(channel)
        # Checks what the channel is
        if str(channel) == "bot-stuff":
            game = "bot-stuff"
            await message.channel.send("What day?")

            # Checks for next message
            def check(m):
                return message.author == m.author and m.channel == channel

            # Sets day based on next message
            day = await client.wait_for("message", check=check)
            await message.channel.send("What time?")
            time = await client.wait_for("message", check=check)
            await message.channel.send("What time zone?")
            time_zone = await client.wait_for("message", check=check)
            await channel.send("Match scheduled for the {}-{}-{} at {} ({})".format(datetime.now().year, datetime.now().month, day.content, time.content, time_zone.content))

            # Create embed for the match info
            embed = discord.Embed(title="New Match!", description="Please schedule this match", )
            embed.add_field(name="Date:", value=f"{datetime.now().year}-{datetime.now().month}-{day.content}")
            embed.add_field(name="Time:", value=f"{time.content} ({time_zone.content})")

            # DM to user the requested date
            user = await client.fetch_user(152535284276264961)
            await user.send(embed=embed)
            await user.send(
                f"Match scheduled for the {datetime.now().year}-{datetime.now().month}-{day.content} at {time.content} ({time_zone.content})")

    if message.content.startswith("$hello"):
        await message.channel.send("Hello")

client.run(token_string)

