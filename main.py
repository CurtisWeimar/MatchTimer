import discord

# T String
token_string = "OTM3NDQ3MjkyNjE1NjU1NTM2.Yfb30w.wbrZVHqig2pP2z9fkU_tgoOL-GE"

# The connection to discord
client = discord.Client()


# Decorator as an event
# on_ready runs when bot is first set up
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


# Fucntion runs
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello")

client.run(token_string)

