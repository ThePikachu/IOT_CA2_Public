from Shared.Database import db
import bcrypt
import time

class User:
	def __init__(self,**kwargs):
		self.Id = kwargs.get('Id', 0)
		self.Username = kwargs.get('Username', "")
		self.Password = kwargs.get('Password', "")
		self.reTypePassword = kwargs.get('reTypePassword', "")
		self.LastLogin = kwargs.get('LastLogin', "")
		self.UserType = kwargs.get('UserType', 0)
		self.CardId = kwargs.get('CardId', "")
		self.ChatId = kwargs.get('ChatId', 0)

	def IsValid(self):
		return self.Username != "" and self.Password != ""

	def IsAdmin(self):
		return self.UserType == 1

	def registerUser(self):
		if self.Username != "" and self.Password != "":
			if self.Password == self.reTypePassword:
				hashed = bcrypt.hashpw(self.Password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
				result = db.insert("insert into users(username,PasswordHash) VALUES('{}','{}')".format(self.Username,hashed))
				return result
			return "2"
		return "1"

	def UpdateLastLogin(self):
		LastLogin = time.strftime('%Y-%m-%d %H:%M:%S')
		db.update("update users set LastLogin = '{}' where Id = {}"
		.format(LastLogin,self.Id))

	def UpdateChatId(self,ChatId):
		db.update("update users set ChatId = {} where Id = {}"
		.format(int(ChatId),self.Id))

	def TryLogin(self):
		result = db.query("select * from users where Username = '{}'"
		.format(self.Username))
		if result == None or len(result) <= 0:
			return False
		StoredHash = result[0]['PasswordHash'].encode("utf-8")
		if bcrypt.hashpw(self.Password.encode("utf-8"),StoredHash) != StoredHash:
			return False
		self.Id = result[0]['Id']
		self.CardId = result[0]['CardId']
		self.UserType = result[0]['UserType']
		self.UpdateLastLogin()
		return True

	@staticmethod
	def ParseFromForm(Form):
		username = Form.get('username')
		password = Form.get('password')
		if username == None: username = ""
		if password == None: password = ""
		return User(Username = username,Password = password)

	@staticmethod
	def ParseRegistrationForm(Form):
		username = Form.get('username')
		password = Form.get('password')
		retypepassword = Form.get('retypepassword')
		if username == None: username = ""
		if password == None: password = ""
		if retypepassword == None: retypepassword = ""
		return User(Username = username,Password = password,reTypePassword = retypepassword)


	@staticmethod
	def TryGetUserById(Id):
		results = db.query("select * from users where Id = {}"
		.format(Id))
		if len(results) <= 0:
			return None
		result = results[0]
		return User(Id = result['Id'],Username = result['Username'],ChatId = result['ChatId'],CardId = result['CardId'])

	@staticmethod
	def GetUsers():
		UsersList = []
		results = db.query("select * from users")
		if len(results) <= 0:
			return None
		for r in results:
			UsersList.append(User(Id = r['Id'],Username = r['Username'],ChatId = r['ChatId'],CardId = r['CardId']))
		return UsersList

	@staticmethod
	def GetChatIdUsers():
		UsersList = []
		results = db.query("select * from users where ChatId is not null")
		if results == None or len(results) <= 0:
			return None
		for r in results:
			UsersList.append(User(Id = r['Id'],Username = r['Username'],ChatId = r['ChatId'],CardId = r['CardId']))
		return UsersList

	@staticmethod
	def TryGetUserByCardId(CardId):
		results = db.query("select * from users where CardId = '{}'"
		.format(CardId))
		if results == None or len(results) <= 0:
			return None
		result = results[0]
		return User(Id = result['Id'],Username = result['Username'],ChatId = result['ChatId'],CardId = result['CardId'])

	@staticmethod
	def addCardId(cardID, userID):
		if (cardID != None):
			id = db.update("update users set cardId =  '{}' where Id = {}".format(cardID, userID))
			return id
		return None
