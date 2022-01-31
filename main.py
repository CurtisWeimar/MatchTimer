import discord
from datetime import datetime
import re

# T String
token_string = "OTM3NDQ3MjkyNjE1NjU1NTM2.Yfb30w.QqD4gPsCAfiz0nDN_uFdL9zjRW8"

# Event Coordinator Discord ID
evt_coord = 216387270972932096

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


def get_game(author):
    match author.id:
        # Zach L
        case 304796852476444673:
            return "Rainbow Six: Siege"
        # Lucas N
        case 322146499775692801:
            return "Rainbow Six: Siege"
        # Pie
        case 251112090285113345:
            return "Rocket League"
        # Scott Rucker
        case 532370983147929600:
            return "Overwatch"
        # Alex M
        case 186863077206130692:
            return "Apex Legends"
        # Mark N
        case 186563647647121408:
            return "League of Legends"
        # Isaac L
        case 377963812730699786:
            return "League of Legends"
        # Lisset S
        case 239936942597341184:
            return "Call of Duty"
        # Brady B
        case 640632283455291423:
            return "Super Smash Brothers: Ultimate"
        # Matthew C
        case 290523728478208002:
            return "Super Smash Brothers: Ultimate"
        # Curtis W
        case 152535284276264961:
            return "Rocket League"
        case _:
            return "No game found for user"


# Function runs when message is sent
@client.event
async def on_message(message):
    # Set what channel we are in
    channel = message.channel

    # Checks if the message is one that a bot sent
    if message.author == client.user:
        return

    author = message.author

    if message.content.startswith("$new"):
        await _new(message=message)

    if message.content.startswith("$hello"):
        await message.channel.send("Hello")


# Generates the embed with info to DM to someone
def game_embed(game, month, day, time, time_zone, streamable):
    embed = discord.Embed(title="New Match!", description="Please schedule this match", color=1752220)
    embed.add_field(name="Game:", value=f"{game}")
    embed.add_field(name="Date:", value=f"{datetime.now().year}-{month}-{day}")
    embed.add_field(name="Time:", value=f"{time} ({time_zone})")
    embed.add_field(name="Streaming?", value=f"{streamable}")
    return embed


# Called when someone wants to schedule a new match
async def _new(message):
    # Assign what channel it was in to a variable
    channel = message.channel
    print(channel)

    # Variables
    month = ""
    day = ""

    game = get_game(message.author)

    # Checks for next message
    def check(m):
        return message.author == m.author and m.channel == channel

    # Send message to user requesting info
    await channel.send("Please enter the match info in the following order:\n"
                       "Date (MM-DD),\n"
                       "Time (XX:XX AM/PM),\n"
                       "Time Zone (mst, est, etc.),\n"
                       "Streamed (Y/N)")
    # Generate blank embed
    blank = blank_embed(message=message)
    temp_embed = await channel.send(embed=blank)

    while True:
        error = False
        # Get the date
        date_response = await client.wait_for("message", check=check)
        date = date_response.content
        # Check date formatting just in case
        error = await check_formatting(channel, date, "date")
        if not error:

            # Temporary date variable to hold list
            _date = date.split("-")
            month = _date[0]
            day = _date[1]

            # Update info on their embed
            blank.remove_field(index=1)
            blank.insert_field_at(index=1, name="Date:", value=f"{datetime.now().year}-{month}-{day}")
            await temp_embed.edit(embed=blank)
        else:
            await channel.message.send("Warning: " + date + " might not match (MM-DD)")

        # Get time and check formatting
        _time = await client.wait_for("message", check=check)
        time = _time.content
        if time is not None:
            error = False

            # Update info on their embed
            blank.remove_field(2)
            blank.insert_field_at(2, name="Date:", value=f"{time}")
            await temp_embed.edit(embed=blank)

        # Get time zone
        _time_zone = await client.wait_for("message", check=check)
        time_zone = _time_zone.content
        if time_zone is not None:
            error = False

            # Update info on their embed
            blank.remove_field(2)
            blank.insert_field_at(2, name="Time:", value=f"{time} ({time_zone})")
            await temp_embed.edit(embed=blank)

        # Get streaming info
        streaming = ""
        streaming_response = await client.wait_for("message", check=check)
        # Check formatting
        if streaming_response.content.lower() == "y":
            streaming = "True"
        elif streaming_response.content.lower() == "n":
            streaming = "False"
        else:
            streaming = "False"
            await channel.send("Warning: Streaming might have been entered wrong.")

        # Update info on their embed
        blank.remove_field(3)
        blank.insert_field_at(3, name="Streaming?", value=f"{streaming}")
        await temp_embed.edit(embed=blank)

        if error is False:
            break

    # Personal discord ID
    me = 152535284276264961
    # if client.get_user(me) == message.author:
    #     game = "Rocket League"

    # Get the game embed
    embed = game_embed(game, month, day, time, time_zone, streaming)
    embed.set_footer(text="Request by: " + str(message.author))

    # DM to user the requested date
    user = await client.fetch_user(me)
    await user.send(embed=embed)
    # await user.send(
    #     f"Match scheduled for the {datetime.now().year}-{datetime.now().month}-{day.content} at {time.content} ({time_zone.content})")


async def check_formatting(channel, string, type):
    match type:
        case "date":
            # If it is formatted right (2 Digits "-" 2 Digits)
            if re.search("\d{1,2}\w{1}\d{1,2}", string) is not None:
                print("Found a '-'")
                return True
            else:
                return False


def blank_embed(message):
    embed = discord.Embed(title="Match Info", description="Please enter the match info:", color=1752220)
    embed.add_field(name="Game:", value=get_game(message.author))
    embed.add_field(name="Date:", value="mm-dd")
    embed.add_field(name="Time:", value="xx:xx")
    embed.add_field(name="Streaming?", value="y/n")
    return embed


client.run(token_string)

