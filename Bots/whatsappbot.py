import sys
import os
sys.path.append(os.path.abspath('..'))
from flask import Flask, render_template, jsonify, request, redirect, url_for,session,send_from_directory
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
from Shared.Database import db
from Shared.Room import Room
from Shared.AccessLog import AccessLog
from Shared.Configs import Config
from Shared.EnviroInfo import EnviroInfo

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
botNum = 'whatsapp:+14155238886'

def sendMessage(message, senderNum):
        message = client.messages.create(from_=botNum,body=message,to=senderNum)

class WhatsAppBot:
    def createMessage(message, senderNum):
        if (message == "/rooms"):
            roomsavailable = []
            allRooms = Room.GetAllRooms();
            for oneRoom in allRooms:
                roomsInfo = AccessLog.GetLatestExitAccessLog(oneRoom.Id)
                if (roomsInfo != None):
                    for x in roomsInfo:
                        if ([x['Exit_time']][0] != None):
                            roomsavailable.append([x['RoomName']][0])
            if roomsavailable == []:
                roomsavailable.append("No Rooms Available")
            messageToSend = "Rooms Available \n"
            availableInString = '\n'.join(roomsavailable)
            messageToSend += availableInString
            sendMessage(messageToSend, senderNum)
        elif (message == "/help"):
            sendMessage("=====All Commands=====\n• /rooms - To see all available rooms\n• /snapshot - To get all IOT Sensor data of all rooms\n", senderNum)
        elif (message == "/snapshot"):
            messageToSend = ""
            roomsList = Room.GetAllRooms()
            for oneRoom in roomsList:
                roomInfo = EnviroInfo.GetLatestEnviroInfo(oneRoom.Id)
                imageUrl = f"{Config.aws_S3_endpoint}snapshot/{oneRoom.Id}.png"
                if (roomInfo is not None):
                    roomMessage = f"=============\nRoom Name: {oneRoom.RoomName}\nLast Updated: {roomInfo['time']}\nTemperature: {roomInfo['temp']}°C" + f"\nHumidity: {roomInfo['humidity']}%\nLight: {roomInfo['light']}\n" + imageUrl + "\n"
                    messageToSend += roomMessage
                    # sendMessage(f"=====\nRoom Name: {oneRoom.RoomName}\nLast Updated: {roomInfo['time']}\nTemperature: {roomInfo['temp']}°C" +
                    #     f"\nHumidity: {roomInfo['humidity']}%\nLight: {roomInfo['light']}\n" + imageUrl, senderNum)
            sendMessage(messageToSend, senderNum)
        else:
            sendMessage("Unknown Command, Type /help for more information.", senderNum)
