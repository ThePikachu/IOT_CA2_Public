from TelegramBot import TelegramBot
from RaspberryPi.AwsIot import AwsIot
from Shared.Room import Room
from time import sleep
import json

awsiot = AwsIot('TeleBot',0)
tele = TelegramBot('')

def MotionEventCallback(client, userdata, message):
    print(message.payload)
    motion_event = json.loads(message.payload)
    tele.NotifyEveryoneRemoteFile(motion_event.get('roomName'),motion_event.get("FilePath"))

awsiot.my_rpi.subscribe('rooms/MotionEvents',1,MotionEventCallback)

while True:
    sleep(1)
