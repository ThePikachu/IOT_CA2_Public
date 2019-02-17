from Shared.Database import db
from Shared.helpers import data_to_json
from Shared.User import User
from Shared.Room import Room

class AccessRight:
	def __init__(self,**kwargs):
		self.Id = int(kwargs.get('Id', 0))
		self.RoomId = int(kwargs.get('RoomId', 0))
		self.UserId = int(kwargs.get('UserId', 0))
		if self.RoomId > 0:
			self.room = Room.TryGetRoomById(self.RoomId)
		else:
			self.room = None
		if self.UserId > 0:
			self.user = User.TryGetUserById(self.UserId)
		else:
			self.user = None

	def IsValidForRemove(self):
		return self.Id > 0

	def IsValidForAdd(self):
		return self.RoomId != 0 and self.UserId != 0

	def IsValidForUpdate(self):
		return self.Id > 0 and self.IsValidForAdd()

	def TryAdd(self):
		if self.HasAccessRight():
			return False
		self.Id = db.insert("insert into access_rights(roomId,userId) VALUES({},{})"
		.format(self.RoomId,self.UserId))
		return self.Id > 0

	def TryUpdateDb(self):
		return db.update("update access_rights set roomId = {}, userId = {} where Id = {}"
		.format(self.RoomId,self.UserId,self.Id))

	def TryRemove(self):
		return db.remove("delete from access_rights where Id = {}"
		.format(self.Id))

	def HasAccessRight(self):
		return len(db.query("SELECT * from access_rights where userId = {} and roomId = {}".format(self.UserId,self.RoomId))) > 0

	@staticmethod
	def ParseFromForm(Form):
		Id = Form.get('Id')
		UserId = Form.get('UserId')
		RoomId = Form.get('RoomId')
		if Id == None: Id = 0
		if UserId == None: UserId = 0
		if RoomId == None: RoomId = 0
		return AccessRight(Id = Id,UserId = UserId,RoomId = RoomId)

	@staticmethod
	def getUserAccessRights(UserId):
		return data_to_json(db.query("SELECT r.RoomName from access_rights ac " +
		"JOIN rooms r ON r.Id = ac.RoomId where ac.UserId = {}".format(UserId)))

	@staticmethod
	def GetAllAccessRights():
		return data_to_json(db.query("SELECT ac.Id, u.Username,u.Id UserId, r.RoomName,r.Id RoomId from access_rights ac " +
		"JOIN users u ON u.Id = ac.UserId " +
		"JOIN rooms r ON r.Id = ac.RoomId"))
