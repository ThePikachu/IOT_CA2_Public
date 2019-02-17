from Shared.Database import db
from Shared.helpers import data_to_json
import time

class EnviroInfo:
	def __init__(self, **kwargs):
		self.Id = kwargs.get('Id', 0)
		self.temp = kwargs.get('temp', 0)
		self.humidity = kwargs.get('humidity', 0)
		self.light_value = kwargs.get('light_value', 0)
		self.time = kwargs.get('time', time.strftime('%Y-%m-%d %H:%M:%S'))
		self.roomId = kwargs.get('roomId', 0)

	def WriteToDb(self):
		self.Id = db.insert("insert into enviro_info(temp,humidity,time,roomId,light_value) VALUES({},{},'{}',{},{})"
		.format(self.temp,self.humidity,self.time,self.roomId,self.light_value))
		if self.Id > 0:
			return True
		else:
			return False

	@staticmethod
	def GetTop10EnviroInfo(RoomId):
		db_results = db.query("SELECT ei.temp, ei.humidity, ei.time FROM enviro_info ei where ei.roomId = {} order by ei.time desc limit 10"
		.format(RoomId))
		results_flipped = db_results[::-1]
		humid = []
		temp = []
		for x in results_flipped:
			humid.append([x['time'],x['humidity']])
			temp.append([x['time'],x['temp']])
		return data_to_json({"temp": temp,"humidity":humid})

	@staticmethod
	def GetAvgEnviroInfoByDay(RoomId):
		db_results = db.query("SELECT Avg(temp) 'AvgTemp', time from enviro_info where roomId = {} group by DAY(time)"
		.format(RoomId))
		humid = []
		temp = []
		for x in db_results:
			temp.append([x['time'],x['AvgTemp']])
		return data_to_json(temp)

	@staticmethod
	def GetLatestEnviroInfo(RoomId):
			db_results = db.query("SELECT ei.temp, ei.humidity, ei.light_value, ei.time FROM enviro_info ei where ei.roomId = {} order by ei.time desc limit 1"
			.format(RoomId))
			if db_results == None or len(db_results) <= 0:
				return None
			result = db_results[0]
			return data_to_json({"time": result['time'], "temp": result['temp'],"humidity": result['humidity'], "light": result['light_value']})
