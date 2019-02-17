from Shared.Database import db
from Shared.helpers import data_to_json
import time

class MotionEvent:
	def __init__(self,**kwargs):
		self.Id = int(kwargs.get('Id', 0))
		self.RoomId = int(kwargs.get('RoomId', 0))
		self.Time = kwargs.get('Time', time.strftime('%Y-%m-%d %H:%M:%S'))
		self.FilePath = kwargs.get('FilePath', "")

	def TryAdd(self):
		self.Id = db.insert("insert into motion_events(RoomId,Time,FilePath) VALUES({},'{}','{}')"
		.format(self.RoomId,self.Time,self.FilePath))
		return self.Id > 0

	def GetDirectory(self):
		index = self.FilePath.rindex("/")
		return self.FilePath[:index]

	def GetFileName(self):
		index = self.FilePath.rindex("/") + 1
		return self.FilePath[index:]

	@staticmethod
	def GetMotionEventsCount():
		results = db.query("select * from motion_events")
		if results == None:
			return 0
		return len(results)

	@staticmethod
	def GetMotionEvents(roomId):
		results = db.query("select me.Id, r.RoomName, me.Time, me.FilePath from motion_events me JOIN rooms r ON me.RoomId = r.Id where me.RoomId = {} order by me.Time desc".format(roomId))
		if results == None or len(results) <= 0:
			return {}
		return results

	@staticmethod
	def GetMotionEventsById(Id):
		results = db.query("select * from motion_events where Id = {}".format(Id))
		if len(results) <= 0:
			return None
		result = results[0]
		return MotionEvent(Id = result["Id"],RoomId = result["RoomId"],Time = result["Time"],FilePath = result["FilePath"])
