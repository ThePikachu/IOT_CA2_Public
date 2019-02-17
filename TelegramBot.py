from Shared.Database import db
import telepot
from Shared.User import User
from Shared.Configs import Config
from Shared.Room import Room
from Shared.AccessLog import AccessLog
from Shared.EnviroInfo import EnviroInfo

class TelegramBot:
	def __init__(self,token):
		self.bot = telepot.Bot(token)
		self.bot.message_loop(self.respondToMsg)
		self.ChatUsers = []
		self.Commands = {
			'NotifyMe': self.DoNotifyMeCommand,
			'RoomAvail': self.DoRoomAvailCommand,
			'RoomSnap': self.DoRoomSnapCommand,
			'CurrentTemp': self.DoCurrentTempCommand
		}

	def respondToMsg(self,msg):
		chat_id = msg['chat']['id']
		command = msg['text']
		print('Got command: {}'.format(command))

		user = self.FindChatUser(chat_id)

		if user == None:
			user = {"Id": chat_id, "CurrentCommand": '', "CommandStep": 0 }
			self.ChatUsers.append(user)

		if len(user['CurrentCommand']) > 0:
			command = user['CurrentCommand']

		if command in self.Commands:
			user['CurrentCommand'] = command
			self.Commands[command](user,msg['text'])
		else:
			result = "Unknown command.\nHi there, here are list of commands to get started.\n"
			index = 1
			for k,v in self.Commands.items():
				result += str(index) + ")"
				index += 1
				result += k + '\n'
			self.bot.sendMessage(user['Id'], result)

	def DoNotifyMeCommand(self,user,text):
		if user['CommandStep'] == 0:
			self.bot.sendMessage(user['Id'], "Please enter your username.")
			user['CommandStep'] = 1
		elif user['CommandStep'] == 1:
			user['Username'] = text
			self.bot.sendMessage(user['Id'], "Please enter your Password.")
			user['CommandStep'] = 2
		elif user['CommandStep'] == 2:
			user['Password'] = text
			U = User(Username = user['Username'], Password = user['Password'])
			if not U.TryLogin():
				self.bot.sendMessage(user['Id'], "Wrong Username or password, please enter username again.")
				user['CommandStep'] = 1
			else:
				user['CommandStep'] = 0
				user['CurrentCommand'] = ""
				U.UpdateChatId(user['Id'])
				self.bot.sendMessage(user['Id'], "Welcome {}, you have been registered to be notified upon motion detection".format(U.Username))

	def DoRoomAvailCommand(self,user,text):
		user['CurrentCommand'] = ""
		rooms = Room.GetAllRooms()
		result = 'Rooms Available:\n'
		for room in rooms:
			if AccessLog.IsRoomAvailable(room.Id):
				result += room.RoomName + '\n'
		self.bot.sendMessage(user['Id'], result)

	def DoRoomSnapCommand(self,user,text):
		if user['CommandStep'] == 0:
			self.bot.sendMessage(user['Id'], "Please enter room name.")
			user['CommandStep'] = 1
		elif user['CommandStep'] == 1:
			user['CommandStep'] = 0
			user['CurrentCommand'] = ""
			rooms = Room.TryGetRoomByRoomName(text)
			if rooms == None or len(rooms) <= 0:
				return self.bot.sendMessage(user['Id'],"Failed to find room: {}".format(text))
			for room in rooms:
				self.bot.sendMessage(user['Id'],"Room Name: {}".format(room.RoomName))
				self.bot.sendDocument(user['Id'], Config.aws_S3_endpoint + 'snapshot/' + str(room.Id) + '.png')

	def DoCurrentTempCommand(self,user,text):
		if user['CommandStep'] == 0:
			self.bot.sendMessage(user['Id'], "Please enter room name.")
			user['CommandStep'] = 1
		elif user['CommandStep'] == 1:
			user['CommandStep'] = 0
			user['CurrentCommand'] = ""
			rooms = Room.TryGetRoomByRoomName(text)
			if rooms == None or len(rooms) <= 0:
				return self.bot.sendMessage(user['Id'],"Failed to find room: {}".format(text))
			for room in rooms:
				self.bot.sendMessage(user['Id'],"Room Name: {}".format(room.RoomName))
				info = EnviroInfo.GetLatestEnviroInfo(room.Id)
				self.bot.sendMessage(user['Id'],"Temp: {} C\nHumidity: {}\nLight: {}\nLast Updated: {}".format(info['temp'],info['humidity'],info['light'],info['time']))

	def NotifyEveryone(self, roomName, VideoPath):
		UserList = User.GetChatIdUsers()
		file_id = 0
		is_document = False
		for user in UserList:
			self.bot.sendMessage(user.ChatId,"Detected motion at {}".format(roomName))
			if file_id <= 0:
				try:
					r = self.bot.sendVideo(user.ChatId, open(VideoPath, 'rb'))
					file_id = r['video']['file_id']
				except KeyError:
					file_id = r['document']['file_id']
					is_document = True
			else:
				if is_document:
					self.bot.sendDocument(chat_id, file_id)
				else:
					self.bot.sendVideo(chat_id, file_id)

	def NotifyEveryoneRemoteFile(self, roomName, VideoPath):
		UserList = User.GetChatIdUsers()
		if UserList == None:
			return
		file_id = 0
		is_document = False
		for user in UserList:
			self.bot.sendMessage(user.ChatId,"Detected motion at {}".format(roomName))
			if file_id <= 0:
				try:
					r = self.bot.sendVideo(user.ChatId, Config.aws_S3_endpoint + VideoPath)
					file_id = r['video']['file_id']
				except KeyError:
					file_id = r['document']['file_id']
					is_document = True
			else:
				if is_document:
					self.bot.sendDocument(chat_id, file_id)
				else:
					self.bot.sendVideo(chat_id, file_id)

	def FindChatUser(self,chat_id):
		for user in self.ChatUsers:
			if user["Id"] == chat_id:
				return user
		return None
