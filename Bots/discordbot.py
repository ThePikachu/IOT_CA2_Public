#using discord.py rewrite version
from discord.ext import commands
import discord, datetime
import sys
import os
sys.path.append(os.path.abspath('..'))
from Shared.Database import db
from Shared.Room import Room
from Shared.AccessLog import AccessLog
from Shared.Configs import Config
from Shared.EnviroInfo import EnviroInfo

bot = commands.Bot(command_prefix="!", status=discord.Status.idle, activity=discord.Game(name="Booting.."))
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} guilds.")
    await bot.change_presence(status=discord.Status.online, activity=(discord.Game(name="Active!")))

@bot.event
async def on_command_error(ctx, error):
    user = ctx.author
    if not isinstance(error, commands.CheckFailure):
        await ctx.channel.send(f"{user.mention}, {error} \nType !help for all commands")

@bot.command()
async def help(ctx):
    await ctx.channel.send(f"========All Commands==========\n• !rooms - To see all available rooms\n• !snapshot - To get all IOT Sensor data of all rooms\n• !ping - To see the latency of the bot")

#test command 1
#!ping
@bot.command()
async def ping(ctx):
    ping_ = bot.latency
    ping = round(ping_ * 1000)
    await ctx.channel.send(f"My ping is {ping}ms")

#test command 2
#!message test
@bot.command()
async def message(ctx, message):
    user = ctx.author
    if message != None:
        await ctx.channel.send(f"{user} sent {message}")
        await ctx.message.delete()

@bot.command()
async def snapshot(ctx):
    roomsList = Room.GetAllRooms()
    await ctx.channel.send(f"Requested by {ctx.author.mention}")
    for oneRoom in roomsList:
        roomInfo = EnviroInfo.GetLatestEnviroInfo(oneRoom.Id)
        imageUrl = f"{Config.aws_S3_endpoint}snapshot/{oneRoom.Id}.png"
        if (roomInfo is not None):
            await ctx.channel.send(f"====================================\nRoom Name: {oneRoom.RoomName}\nLast Updated: {roomInfo['time']}\nTemperature: {roomInfo['temp']}°C" +
                f"\nHumidity: {roomInfo['humidity']}%\nLight: {roomInfo['light']}\n" + imageUrl)
    await ctx.message.delete()

#get available rooms
#!rooms
@bot.command()
async def rooms(ctx):
    currentDT = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    roomsavailable = []
    allRooms = Room.GetAllRooms();
    for oneRoom in allRooms:
        roomsInfo = AccessLog.GetLatestExitAccessLog(oneRoom.Id)
        if (roomsInfo != None):
            for x in roomsInfo:
                if ([x['Exit_time']][0] != None):
                    roomsavailable.append([x['RoomName']])
    if roomsavailable == []:
        roomsavailable.append("No Rooms Available")
    await ctx.channel.send(f"=====================\nTime Requested: {currentDT} \nRequested By: {ctx.author.mention} \nRooms available: {roomsavailable}\n=====================")
    #delete command message
    await ctx.message.delete()

# @bot.command()
# async def subscribe(ctx, member):
#     await ctx.message.delete()
#
# @bot.command()
# async def unsubscribe(ctx):
#     await ctx.message.delete()

#shut down the bot
@bot.command()
async def s(ctx):
    await bot.close()

bot.run("")
