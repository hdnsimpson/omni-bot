import discord
import asyncio
import time
import youtube_dl
import requests

from discord.ext.commands import bot
from discord.ext import commands
from features import *

Client = discord.Client()
client = commands.Bot(command_prefix = "!")

creatorID = "209541973097447424"
token = "NDQ5NDc5NTM4NzQxNzM5NTIw.DelS4A.150chag8hxlGzjBvlw0rEeQ-35Q"

chatFilter = False

# Reports when bot is ready
@client.event
async def on_ready():
    print('manny-bot logged in')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))
    print('Invite URL: ' + 'https://discordapp.com/api/oauth2/authorize?client_id=' + client.user.id + '&permissions=8&scope=bot\n')

# Message listens / Commands
@client.event
async def on_message(message):
    userID = message.author.id
    contents = message.content.split(" ")
    global chatFilter


    ########## CHAT FILTER ##########

    # Enable chat filter
    if message.content.upper() == "!FILTERON":
        chatFilter = True
        await client.send_message(message.channel, "Chat filter enabled")

    # Disable chat filter
    if message.content.upper() == "!FILTEROFF":
        chatFilter = False
        await client.send_message(message.channel, "Chat filter disabled")
    
    # Filter chat
    for word in contents:
        if word.lower() in bannedWords.words and chatFilter == True:
            try:
                await client.delete_message(message)
                await client.send_message(message.channel, "<@%s>'s message was deleted for containing a banned word" % userID)
            except discord.errors.NotFound:
                return

    # Manny status
    if message.content.upper() == "!OMNI":
        await client.send_message(message.channel, "Omni awaiting command")

    # Ping - Pong to user
    if message.content.upper().startswith("!PING"):
        await client.send_message(message.channel, "<@%s> Pong!" % (userID))

    # Say user input, if prompted by me
    if message.content.upper().startswith("!SAY"):
        if message.author.id == creatorID:
            await client.send_message(message.channel, "%s" % (" ".join(contents[1:])))
        else:
            await client.send_message(message.channel, "<@%s> does not have permission for this command" % (userID))

    # Use text to speech
    if message.content.upper().startswith("!SHOUT"):
        await client.send_message(message.channel, "%s" % (" ".join(contents[1:])), tts=True)

    # Check if user is an admin
    if message.content.upper().startswith("!AMIADMIN"):
        if "447609385641050122" in [role.id for role in message.author.roles]:
            await client.send_message(message.channel, "<@%s> is an admin" % (userID))
        else:
            await client.send_message(message.channel, "<@%s> is not an admin" % (userID))



    ########## VOICE CHANNEL COMMANDS ##########

    # Join bot to a voice channel
    if message.content.upper().startswith("!JOIN"):
        if message.author.voice_channel != None and client.is_voice_connected(message.server) != True:
            global player
            global currentChannel
            global voice
            currentChannel = client.get_channel(message.author.voice_channel.id)
            voice = await client.join_voice_channel(currentChannel)
        elif message.author.voice_channel == None:
            await client.send_message(message.channel, "You must be in a voice channel to use !join")
        else:
            await client.send_message(message.channel, "I am already in a voice channel, use !leave to make me leave")

    # Make the bot leave a voice channel
    if message.content.upper().startswith("!LEAVE"):
        if client.is_voice_connected(message.server):
            currentChannel = client.voice_client_in(message.server)
            await currentChannel.disconnect()



    ########## YOUTUBE INTEGRATION ##########
    
    # Play a youtube video's audio with a url/key words
    if message.content.upper().startswith("!PLAY"):
        if message.author.voice_channel != None:
            if client.is_voice_connected(message.server) == True:
                try:
                    if player.is_playing() == False:
                        player = await voice.create_ytdl_player(youtubeLink.getYoutubeLink(message.content))
                        player.start()
                        await client.send_message(message.channel, ":musical_note: Now playing: " + player.title)
                except NameError:
                    player = await voice.create_ytdl_player(youtubeLink.getYoutubeLink(message.content))
                    player.start()
                    await client.send_message(message.channel, ":musical_note: Now playing: " + player.title)
            else:
                await client.send_message(message.channel, "I am not connected to a voice channel, use !join")
        else:
            await client.send_message(message.channel, "You are not connected to a voice channel, use !join once you are")

    # Pause the youtube player
    if message.content.upper().startswith("!PAUSE"):
        try:
            player.pause()
        except NameError:
            await client.send_message(message.channel, "Not currently playing audio")

    # Resume the youtube player
    if message.content.upper().startswith("!RESUME"):
        try:
            player.resume()
        except NameError:
            await client.send_message(message.channel, "Not currently playing audio")

    # Stop the youtube player
    if message.content.upper().startswith("!STOP"):
        try:
            player.stop()
        except NameError:
            await client.send_message(message.channel, "Not currently playing audio")

    # Change the volume of the youtube player
    if message.content.upper().startswith("!VOLUME"):
        try:
            player.volume = int(contents[1]) / 100
        except NameError:
            await client.send_message(message.channel, "Not currently playing audio")
        except ValueError:
            await client.send_message(message.channel, "Correct usage is !volume [integer relating to volume percentage]")

    # Play a youtube video with a url/key words
    if message.content.upper().startswith("!SEARCHVID"):
        await client.send_message(message.channel, youtubeLink.getYoutubeLink(message.content[5:]))



                


# Run the bot
client.run(token)

