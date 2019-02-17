from Shared.Room import Room
from Shared.EnviroInfo import EnviroInfo
import socket
import Adafruit_DHT
from time import sleep
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import datetime as datetime
from Shared.helpers import data_to_json
import json
from gpiozero import MCP3008
from AwsIot import AwsIot

room = Room.TryGetRoom(socket.gethostname())

if room == None:
	print("Failed to get room")
	exit()

logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

aws = AwsIot('room_updater' + str(room.Id),-1)
adc = MCP3008(channel=0)

while True:
	humidity, temperature = Adafruit_DHT.read_retry(11, 4)
	print('Temp: {:.1f} C'.format(temperature))
	print('Humidity: {:.1f}'.format(humidity))
	light = adc.value * 1024
	print('light_value: {}'.format(light))
	en_info = EnviroInfo(roomId = room.Id, temp = temperature,humidity = humidity,light_value = light)
	en_info.WriteToDb()
	message = {}
	message["time"] = datetime.datetime.now()
	message["temp"] = temperature
	message["humid"] = humidity
	aws.my_rpi.publish("rooms/" + str(room.Id) + "/enviroData", json.dumps(data_to_json(message)), 0)

	sleep(5)
