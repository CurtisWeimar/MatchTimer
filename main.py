import discord

# T String
string = "OTM3NDQ3MjkyNjE1NjU1NTM2.Yfb30w.9oCgK_DpRO6QE82SAaPNC2CgDT0"

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

client.run(string)

