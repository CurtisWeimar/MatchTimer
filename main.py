import discord
from datetime import datetime
import re

# T String
# noinspection SpellCheckingInspection
token_string = "token_string_here"

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


# @client.event
# async def on_raw_reaction_add(reaction):
#     msg = reaction
#     print(reaction.message_id)


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


# TODO: Create / commands
# Function runs when message is sent
@client.event
async def on_message(message):

    # Checks if the message is one that a bot sent
    if message.author == client.user:
        return

    if message.content.startswith("$new"):
        await _new(message=message)

    if message.content.startswith("$hello"):
        await message.channel.send("Hello")

    if message.content.startswith("$update"):
        await _update(message=message)

    if message.content.startswith("$remove"):
        await _remove(message=message)


# TODO: Combine embed methods with a "type" to combine embed creation into one method
# Generates the embed with info to DM to someone
def game_embed(game, date, time, time_zone, streamable):
    embed = discord.Embed(title="New Match!", description="Please schedule this match", color=1752220)
    embed.add_field(name="Game:", value=f"{game}")
    embed.add_field(name="Date:", value=f"{datetime.now().year}-{date}")
    embed.add_field(name="Time:", value=f"{time} ({time_zone})")
    embed.add_field(name="Streaming?", value=f"{streamable}")
    return embed


# Generates the embed with info to DM to someone for updating
def upd_game_embed(game, date, time, time_zone, streamable):
    embed = discord.Embed(title="Match Change!", description="Please change this match's schedule", color=15548997)
    embed.add_field(name="Game:", value=f"{game}")
    embed.add_field(name="Date:", value=f"{datetime.now().year}-{date}")
    embed.add_field(name="Time:", value=f"{time} ({time_zone})")
    embed.add_field(name="Streaming?", value=f"{streamable}")
    return embed


# TODO: Add in preview embed + change embed color
async def _remove(message):
    channel = message.channel

    game = get_game(message.author)

    # Checks for next message
    def check(m):
        return message.author == m.author and m.channel == channel

    await channel.send("Please enter the match info in the following order:\n"
                       "Date (MM-DD),\n")

    date_response = await client.wait_for("message", check=check)
    date = date_response.content

    error = check_formatting(type="date", string=date)

    if error:
        await message.channel.send("Warning: '" + date + "' might not match (MM-DD)!")

    # TODO: Move embed creation to combined embed method
    embed = discord.Embed(title="Match Removal!", description="Please remove the match for this day", color=15548997)
    embed.add_field(name="Game:", value=game)
    embed.add_field(name="Date:", value=date)

    # Personal discord ID
    me = 152535284276264961

    # DM to user the requested date
    user = await client.fetch_user(me)
    await user.send(embed=embed)


async def _update(message):
    channel = message.channel

    game = get_game(message.author)

    # Checks for next message
    def check(m):
        return message.author == m.author and m.channel == channel

    # Send message to user requesting info
    await channel.send("Please enter the match info in the following order:\n"
                       "Old Date (MM-DD),\n"
                       "New Date (MM-DD),\n"
                       "New Time (XX:XX AM/PM),\n"
                       "Time Zone (mst, est, etc.),\n"
                       "Streamed (Y/N)")

    # Generate blank embed to store their input
    blank = blank_embed(message=message)
    blank.insert_field_at(index=1, name="Old Date:", value="mm-dd")  # Some fields are added for update embed
    blank.remove_field(index=2)
    blank.insert_field_at(index=2, name="New Date:", value="mm-dd")
    blank.set_footer(text="Request by: " + str(message.author))  # Insert footer
    temp_embed = await channel.send(embed=blank)

    old_date_response = await client.wait_for("message", check=check)
    old_date = old_date_response.content

    # Check date formatting just in case
    error = check_formatting(old_date, "date")
    print(error)
    if error:
        await message.channel.send("Warning: '" + old_date + "' might not match (MM-DD)!")

    blank.remove_field(index=1)
    blank.insert_field_at(index=1, name="Old Date:", value=f"{datetime.now().year}-{old_date}")
    await temp_embed.edit(embed=blank)

    date_response = await client.wait_for("message", check=check)
    date = date_response.content

    # Check date formatting just in case
    error = check_formatting(date, "date")
    print(error)
    if error:
        await message.channel.send("Warning: '" + date + "' might not match (MM-DD)!")

    blank.remove_field(index=2)
    blank.insert_field_at(index=2, name="New Date:", value=f"{datetime.now().year}-{date}")
    await temp_embed.edit(embed=blank)

    # TODO: Put in time formatting
    # Get time and check formatting
    _time = await client.wait_for("message", check=check)
    time = _time.content
    if time is not None:
        error = False

        if error:
            await message.channel.send("Warning: '" + time + "' might not match (XX:XX)!")
        blank.remove_field(3)
        blank.insert_field_at(3, name="Date:", value=f"{time}")
        await temp_embed.edit(embed=blank)

    # Get time zone
    _time_zone = await client.wait_for("message", check=check)
    time_zone = _time_zone.content
    if time_zone is not None:
        error = False
        if error:
            await message.channel.send("Warning: '" + time_zone + "' might not be formatted properly!")
        # Update their embed
        blank.remove_field(3)
        blank.insert_field_at(3, name="Time:", value=f"{time} ({time_zone})")
        await temp_embed.edit(embed=blank)

    # Get streaming info
    streaming = ""
    streaming_response = await client.wait_for("message", check=check)
    # Check formatting
    # TODO: Move formatting check into the proper method
    if streaming_response.content.lower() == "y":
        streaming = "True"
    elif streaming_response.content.lower() == "n":
        streaming = "False"
    else:
        streaming = "False"
        await channel.send("Warning: Streaming info may have been entered wrong!.")

    # Update info on their embed
    blank.remove_field(4)
    blank.insert_field_at(4, name="Streaming?", value=f"{streaming}")
    await temp_embed.edit(embed=blank)

    # Personal discord ID
    me = 152535284276264961

    # Get the game embed
    print(old_date)
    embed = upd_game_embed(game, date, time, time_zone, streaming)
    embed.insert_field_at(index=1, name="Old Date:", value=f"{datetime.now().year}-{old_date}")
    embed.set_footer(text="Request by: " + str(message.author))

    # DM to user the requested date
    user = await client.fetch_user(me)
    await user.send(embed=embed)


# TODO: Create methods to remove some of the code from this. Already starting to me unreadable
# TODO: Remove while loop. It isn't necessary
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
    blank.set_footer(text="Request by: " + str(message.author))  # Insert footer
    temp_embed = await channel.send(embed=blank)

    while True:
        error = False
        # Get the date
        date_response = await client.wait_for("message", check=check)
        date = date_response.content
        # Check date formatting just in case
        error = check_formatting(date, "date")
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
            await message.channel.send("Warning: '" + date + "' might not match (MM-DD)")
            blank.remove_field(index=1)
            blank.insert_field_at(index=1, name="Date:", value=f"{datetime.now().year}-{month}-{day}")
            await temp_embed.edit(embed=blank)

        # TODO: Put in time formatting
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
    embed = game_embed(game, date, time, time_zone, streaming)
    embed.set_footer(text="Request by: " + str(message.author))

    # DM to user the requested date
    user = await client.fetch_user(me)
    await user.send(embed=embed)
    # await user.send(
    #     f"Match scheduled for the {datetime.now().year}-{datetime.now().month}-{day.content} at {time.content} ({time_zone.content})")


# TODO: Create formatting checks for other entries
def check_formatting(string, type):
    match type:
        case "date":
            # If it is formatted right (2 Digits "-" 2 Digits)
            regex = "\d{1,2}-\d{1,2}"
            if re.search(regex, string) is not None:
                print("Found a '-'")
                return False
            else:
                return True


# TODO: Move to embed method
def blank_embed(message):
    embed = discord.Embed(title="Match Info", description="Please enter the match info:", color=1752220)
    embed.add_field(name="Game:", value=get_game(message.author))
    embed.add_field(name="Date:", value="mm-dd")
    embed.add_field(name="Time:", value="xx:xx")
    embed.add_field(name="Streaming?", value="y/n")
    return embed


client.run(token_string)
