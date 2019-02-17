import os
from Shared.MotionEvent import MotionEvent
from gpiozero import MotionSensor
from gpiozero import Buzzer
from picamera import PiCamera
from AwsS3 import AwsS3
import time

class MotionDetection:
	def __init__(self, BasePath, TelgramId, room):
		print("Initializing Camera")
		self.camera = PiCamera()
		self.camera.resolution = (640, 480)
		print("Initializing AWS")
		self.s3 = AwsS3()
		print("Initializing MotionSensor")
		self.pir = MotionSensor(26, sample_rate=1000,queue_len=1,threshold=0.9)
		self.pir.when_motion = self.OnMotion
		self.pir.when_no_motion = self.OnStopMotion

		self.bz = Buzzer(21)

		self.DisarmDetector = False
		self.has_detected_motion = False
		self.BasePath = BasePath
		self.room = room
		self.MotionCallback = None

		if not os.path.isdir(BasePath):
			os.makedirs(BasePath)

		self.update_time = time.time()
		self.snapshot_file_path = str(room.Id) + '.png'

	def SaveRecording(self):
		self.camera.stop_recording()
		video_file_name = "video{}.mp4".format(self.video_index)
		vid_path = self.BasePath + "/" + video_file_name
		os.system("MP4Box -add " + self.BasePath + "/video0.h264 " + vid_path)
		s3_path = 'videos/' + video_file_name
		self.s3.Upload(vid_path,s3_path)
		if self.MotionCallback:
			self.MotionCallback(s3_path)
		self.has_detected_motion = False
		self.bz.off()

	def OnMotion(self):
		if not self.DisarmDetector:#record
			print("Motion detected")
			if self.has_detected_motion:
				self.SaveRecording()
			self.has_detected_motion = True
			self.video_index = MotionEvent.GetMotionEventsCount()
			File = 'videos/video{}.mp4'.format(self.video_index)
			ME = MotionEvent(RoomId = self.room.Id,FilePath = File)
			ME.TryAdd()
			self.camera.start_recording(self.BasePath + '/video0.h264')
			self.bz.on()

	def OnStopMotion(self):
		if not self.DisarmDetector and self.has_detected_motion:#stop recording
			print("Motion stopped")
			self.SaveRecording()
		elif self.DisarmDetector and self.has_detected_motion:
			print("Motion stopped")
			self.SaveRecording()

	def UpdateCameraSnapshot(self):
		if time.time() - self.update_time < 5:
			return
		self.update_time = time.time()
		my_file = open(self.snapshot_file_path, 'wb')
		try:
			self.camera.capture(my_file)
		except:
			print("encounter issue with camera")
			self.camera.close()
			self.camera = PiCamera()
			self.camera.resolution = (640, 480)

		my_file.close()
		self.s3.Upload(self.snapshot_file_path,'snapshot/' + self.snapshot_file_path)

	def SetCallbackForMotion(self,Callback):
		self.MotionCallback = Callback
