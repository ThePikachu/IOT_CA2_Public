## Set Initial Variables ##
import os # Miscellaneous operating system interface
import zmq # Asynchronous messaging framework
import time # Time access and conversions
from random import randint # Random numbers
import sys # System-specific parameters and functions
from matrix_io.proto.malos.v1 import driver_pb2 # MATRIX Protocol Buffer driver library
from matrix_io.proto.malos.v1 import io_pb2 # MATRIX Protocol Buffer sensor library
from multiprocessing import Process, Manager, Value # Allow for multiple processes at once
from zmq.eventloop import ioloop, zmqstream# Asynchronous events through ZMQ
from utils import register_error_callback
from AwsIot import AwsIot
from Shared.Room import Room
import socket
import json

matrix_ip = '127.0.0.1' # Local device ip
everloop_port = 20021 # Driver Base port
led_count = 0 # Amount of LEDs on MATRIX device
led_switch = False

room = Room.TryGetRoomByLight(socket.gethostname())

if room == None:
	print("Failed to get room")
	exit()

awsiot = AwsIot('room_light' + str(room.Id),0)
rgb_color = None

def customCallback(client, userdata, message):
	print("GOT CALLBACK")
	print(message.payload)
	global led_switch
	if message.payload == "1":
		led_switch = True
	else:
		led_switch = False

def colourChangeCallback(client, userdata, message):
	global rgb_color
	print(message.payload)
	rgb_color = json.loads(message.payload)

awsiot.my_rpi.subscribe('rooms/' + str(room.Id) + '/LightSwitch', 1, customCallback)
awsiot.my_rpi.subscribe('rooms/' + str(room.Id) + '/ColourChange', 1, colourChangeCallback)

def config_socket(ledCount):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect('tcp://{0}:{1}'.format(matrix_ip, everloop_port))

    while True:
		driver_config_proto = driver_pb2.DriverConfig()
		image = []
		light_value = 0
		global led_switch
		global rgb_color
		if led_switch:
			light_value = 255
		for led in range(ledCount):
			ledValue = io_pb2.LedValue()
			if rgb_color and led_switch:
				ledValue.blue = rgb_color.get('b')
				ledValue.red = rgb_color.get('r')
				ledValue.green = rgb_color.get('g')
				ledValue.white = 0
			else:
				ledValue.blue = light_value
				ledValue.red = light_value
				ledValue.green = light_value
				ledValue.white = 0
			image.append(ledValue)
		driver_config_proto.image.led.extend(image)

		socket.send(driver_config_proto.SerializeToString())
		time.sleep(0.05)

def ping_socket():
    context = zmq.Context()
    ping_socket = context.socket(zmq.PUSH)
    ping_socket.connect('tcp://{0}:{1}'.format(matrix_ip, everloop_port+1))
    ping_socket.send_string('')

def everloop_error_callback(error):
    print('{0}'.format(error))

## DATA UPDATE PORT ##
def update_socket():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://{0}:{1}'.format(matrix_ip, everloop_port+3))
    socket.setsockopt(zmq.SUBSCRIBE, b'')
    stream = zmqstream.ZMQStream(socket)
    def updateLedCount(data):
        global led_count
        led_count = io_pb2.LedValue().FromString(data[0]).green
        print('{0} LEDs counted'.format(led_count))
        if led_count > 0:
            ioloop.IOLoop.instance().stop()
            print('LED count obtained. Disconnecting from data publisher {0}'.format(everloop_port+3))
    stream.on_recv(updateLedCount)
    print('Connected to data publisher with port {0}'.format(everloop_port+3))
    ioloop.IOLoop.instance().start()

## START  PROCESSES ##
if __name__ == '__main__':
    ioloop.install()
    Process(target=register_error_callback, args=(everloop_error_callback, matrix_ip, everloop_port)).start()
    ping_socket()
    update_socket()
    try:
        config_socket(led_count)
    except KeyboardInterrupt:
        print(' quit')
