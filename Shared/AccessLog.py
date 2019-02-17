from Shared.Database import db
from Shared.helpers import data_to_json
from Shared.Room import Room
import time

class AccessLog:
	def __init__(self,**kwargs):
		self.Id = int(kwargs.get('Id', 0))
		self.RoomId = int(kwargs.get('RoomId', 0))
		self.UserId = kwargs.get('UserId', "")
		self.Time = kwargs.get('Time', time.strftime('%Y-%m-%d %H:%M:%S'))
		self.ExitTime = kwargs.get('ExitTime', "")
		self.IsValid = kwargs.get('IsValid', False)
		if self.RoomId > 0:
			self.room = Room.TryGetRoomById(self.RoomId)
		else:
			self.room = None

	def UpdateExitTime(self):
		self.ExitTime = time.strftime('%Y-%m-%d %H:%M:%S')
		self.TryUpdateDb()

	def TryAdd(self):
		self.Id = db.insert("insert into access_logs(RoomId,UserId,Time,IsValid) VALUES({},'{}','{}',{})"
		.format(self.RoomId,self.UserId,self.Time,self.IsValid))
		return self.Id > 0

	def TryUpdateDb(self):
		return db.update("update access_logs set Exit_time = '{}' where Id = {}"
		.format(self.ExitTime,self.Id))

	@staticmethod
	def GetAccessLogForRoom(RoomId):
		db_results = db.query("select * from access_logs where RoomId = {} order by Time".format(RoomId))
		if db_results == None or len(db_results) <= 0:
			return {}
		return db_results

	@staticmethod
	def GetValidExitedAccessLogForRoom(RoomId):
		db_results = db.query("SELECT r.RoomName, u.Username, al.Time, al.Exit_time FROM access_logs al " +
		"JOIN rooms r on al.RoomId = r.Id " +
		"JOIN users u on al.UserId = u.Id " +
		"where al.RoomId = {} and al.IsValid = 1 order by al.Time desc".format(RoomId))
		if db_results == None or len(db_results) <= 0:
			return {}
		return db_results

	@staticmethod
	def GetInvalidExitedAccessLogForRoom(RoomId):
		db_results = db.query("SELECT r.RoomName, u.Username, al.Time FROM access_logs al " +
		"JOIN rooms r on al.RoomId = r.Id " +
		"JOIN users u on al.UserId = u.Id " +
		"where al.RoomId = {} and al.IsValid = 0 order by al.Time desc".format(RoomId))
		if db_results == None or len(db_results) <= 0:
			return {}
		return db_results

	@staticmethod
	def GetLatestExitAccessLog(RoomId):
		db_results = db.query("SELECT r.RoomName,al.Id, al.Time, al.Exit_time FROM access_logs al " +
			"JOIN rooms r on al.RoomId = r.Id where al.IsValid = 1 and al.RoomId = {} order by al.Id desc LIMIT 1"
			.format(RoomId))
		if db_results == None or len(db_results) <= 0:
			return {}
		return db_results

	@staticmethod
	def IsRoomAvailable(RoomId):
		db_results = db.query("SELECT * FROM access_logs al " +
		"where al.RoomId = {} and al.IsValid = 1 and al.Exit_time is null".format(RoomId))
		if db_results == None or len(db_results) <= 0:
			return True
		return False
