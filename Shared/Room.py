from Shared.Database import db
from Shared.helpers import data_to_json

class Room:
	def __init__(self,**kwargs):
		self.Id = int(kwargs.get('Id', 0))
		self.RoomName = kwargs.get('RoomName', "")
		self.IotDeviceName = kwargs.get('IotDeviceName', "")
		self.IoTLightDevice = kwargs.get('IoTLightDevice', "")

	def IsValidForAdd(self):
		return self.RoomName != "" and self.IotDeviceName != ""

	def IsValidForUpdate(self):
		return self.Id > 0 and self.IsValidForAdd()

	def TryAdd(self):
		self.Id = db.insert("insert into rooms(RoomName,IotDeviceName,IoTLightDevice) VALUES('{}','{}','{}')"
		.format(self.RoomName,self.IotDeviceName,self.IoTLightDevice))
		return self.Id > 0

	def TryUpdateDb(self):
		return db.update("update rooms set RoomName = '{}', IotDeviceName = '{}', IoTLightDevice = '{}' where Id = {}"
		.format(self.RoomName,self.IotDeviceName,self.IoTLightDevice,self.Id))

	def TryRemove(self):
		return db.remove("delete from rooms where Id = {}"
		.format(self.Id))

	@staticmethod
	def ParseFromForm(Form):
		Id = Form.get('IotId')
		RoomName = Form.get('RoomName')
		IotDeviceName = Form.get('IotDeviceName')
		IoTLightDevice = Form.get('IoTLightDevice')
		if Id == None: Id = 0
		if RoomName == None: RoomName = ""
		if IotDeviceName == None: IotDeviceName = ""
		return Room(Id = Id,RoomName = RoomName,IotDeviceName = IotDeviceName,IoTLightDevice = IoTLightDevice)

	@staticmethod
	def TryGetRoom(DeviceName):
		results = db.query("select * from rooms where IotDeviceName = '{}'"
		.format(DeviceName))
		if len(results) <= 0:
			return None
		result = results[0]
		return Room(Id = result["Id"],RoomName = result["RoomName"],IotDeviceName = result["IotDeviceName"],IoTLightDevice = result["IoTLightDevice"])

	@staticmethod
	def TryGetRoomByLight(DeviceName):
		results = db.query("select * from rooms where IoTLightDevice = '{}'"
		.format(DeviceName))
		if len(results) <= 0:
			return None
		result = results[0]
		return Room(Id = result["Id"],RoomName = result["RoomName"],IotDeviceName = result["IotDeviceName"],IoTLightDevice = result["IoTLightDevice"])

	@staticmethod
	def TryGetRoomById(Id):
		results = db.query("select * from rooms where Id = {}"
		.format(Id))
		if results == None or len(results) <= 0:
			return None
		result = results[0]
		return Room(Id = result["Id"],RoomName = result["RoomName"],IotDeviceName = result["IotDeviceName"],IoTLightDevice = result["IoTLightDevice"])

	@staticmethod
	def GetAllRoomsJSON():
		return data_to_json(db.query("select * from rooms"))

	@staticmethod
	def GetAllRooms():
		RoomsList = []
		results = db.query("select * from rooms")
		if results == None or len(results) <= 0:
			return None
		for r in results:
			RoomsList.append(Room(Id = r["Id"],RoomName = r["RoomName"],IotDeviceName = r["IotDeviceName"],IoTLightDevice = r["IoTLightDevice"]))
		return RoomsList

	@staticmethod
	def TryGetRoomByRoomName(RoomName):
		RoomsList = []
		results = db.query("select * from rooms where lower(RoomName) = '{}'".format(RoomName.lower()))
		if results == None or len(results) <= 0:
			return None
		for r in results:
			RoomsList.append(Room(Id = r["Id"],RoomName = r["RoomName"],IotDeviceName = r["IotDeviceName"],IoTLightDevice = r["IoTLightDevice"]))
		return RoomsList
