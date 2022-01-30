import discord

# T String
token_string = "OTM3NDQ3MjkyNjE1NjU1NTM2.Yfb30w.QqD4gPsCAfiz0nDN_uFdL9zjRW8"

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
    print("We have logged in as {0.user}".format(client))


# Fucntion runs
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

            def check(m):
                return message.author == m.author and m.channel == channel

            day = await client.wait_for("message", check=check)
            await channel.send("Match scheduled for the {}".format(day.content))

    if message.content.startswith("$hello"):
        await message.channel.send("Hello")

client.run(token_string)

