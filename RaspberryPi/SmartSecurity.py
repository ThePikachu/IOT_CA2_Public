import socket
from Shared.Room import Room
from LCDScroller import LCDScroller
from time import sleep
import RPi.GPIO as GPIO
import MFRC522
import signal
from Shared.User import User
from Shared.AccessRight import AccessRight
from Shared.AccessLog import AccessLog
from MotionDetection import MotionDetection
from Shared.Database import db
import thread
from AwsIot import AwsIot
import json

room = Room.TryGetRoom(socket.gethostname())
access_right = None
access_user = None
access_log = None
mfrc522 = MFRC522.MFRC522()
lcd = LCDScroller()

if room == None:
	print("Failed to get room")
	exit()

awsiot = AwsIot('room' + str(room.Id),2)
awsiot_topic = 'rooms/' + str(room.Id) + '/LightSwitch'

def OnMotionEvent(VideoPath):
	global awsiot
	message = {
		'roomName': room.RoomName,
		'FilePath': VideoPath
	}
	json_data = json.dumps(message)
	awsiot.my_rpi.publish('rooms/MotionEvents',json_data,1)

md = MotionDetection('/home/pi/labs/CA2/recordings','587634217:AAGfWPAPbd6GV91XL5g6gszCZec06WsiXJo',room)
md.SetCallbackForMotion(OnMotionEvent)

#---------------------------------------------------------------------------------

continue_reading = True
def end_read(signal,frame):
	global continue_reading
	print "Ctrl+C captured, ending read."
	db.Continue = False
	print("stopping camera")
	md.camera.close()
	continue_reading = False
	GPIO.setmode(GPIO.BCM)
	GPIO.cleanup(25)

signal.signal(signal.SIGINT, end_read)

def snapshot_thread():
	global continue_reading
	global md
	while continue_reading:
		sleep(5)
		md.UpdateCameraSnapshot()

thread.start_new_thread(snapshot_thread, ())
#---------------------------------------------------------------------------------

def ShowDefault():
	lcd.text(room.RoomName, 1)
	lcd.text('Tap card to access.',2)

def ShowWelcomeMsg():
	lcd.clear()
	lcd.text("Welcome {}".format(access_right.user.Username),1)

#---------------------------------------------------------------------------------

ShowDefault()

while continue_reading:
	(status,TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)
	if status == mfrc522.MI_OK:
		(status,uid) = mfrc522.MFRC522_Anticoll()
		print("New card detected! UID of card is {}".format(uid))
		if access_right == None:
			access_user = User.TryGetUserByCardId(uid)
			if access_user != None:
				access_right = AccessRight(RoomId = room.Id,UserId = access_user.Id)
				if not access_right.HasAccessRight():
					access_right = None
			md.DisarmDetector = access_right != None
			lcd.clear()
			if access_right == None:
				lcd.text("Card rejected!",1)
				lcd.text("Please try again!",2)
				if access_user != None:
					Invalid_al = AccessLog(RoomId = room.Id,UserId = access_user.Id,IsValid = False)
					Invalid_al.TryAdd()
				sleep(3)
				ShowDefault()
			else:
				access_log = AccessLog(RoomId = room.Id,UserId = access_user.Id,IsValid = True)
				access_log.TryAdd()
				ShowWelcomeMsg()
				awsiot.my_rpi.publish(awsiot_topic,"1",1)
				sleep(3)
		elif access_user.CardId == str(uid):
			access_right = None
			md.DisarmDetector = False
			access_log.UpdateExitTime()
			access_log = None
			lcd.clear()
			lcd.text("Thank you.",1)
			lcd.text("Have a nice day.",2)
			while not awsiot.my_rpi.publish(awsiot_topic,"0",1):
				sleep(1)
			sleep(3)
			ShowDefault()
		else:
			lcd.clear()
			lcd.text("Please use back old",1)
			lcd.text("card to lock",2)
			sleep(3)
			ShowWelcomeMsg()
	sleep(0.2)
	if not continue_reading:
		exit()
	lcd.update()
