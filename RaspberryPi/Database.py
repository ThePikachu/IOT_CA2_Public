import mysql.connector
import sys
from Shared.Configs import Config

class Database:
	def __init__(self):
		self.Init()
		self.Continue = True

	def Init(self):
		try:
			self.cnx = mysql.connector.connect(host=Config.db_host,user=Config.db_user,password=Config.db_password
			,database=Config.databaseName,autocommit=True)
			print("Successfully connected to database!")
		except:
			print(sys.exc_info()[0])
			print(sys.exc_info()[1])
			if not self.Continue:
				return 0
			self.Init()

	def query(self,sql):
		try:
			cursor = self.cnx.cursor(buffered=True)
			cursor.execute(sql)
			row_headers=[x[0] for x in cursor.description]
			results = cursor.fetchall()
			data = []
			for result in results:
				data.append(dict(zip(row_headers,result)))
			return data
		except:
			print(sys.exc_info()[0])
			print(sys.exc_info()[1])
			if not self.Continue:
				return 0
			self.Init()
			return self.query(sql)

	def insert(self,sql):
		try:
			cursor = self.cnx.cursor()
			cursor.execute(sql)
			self.cnx.commit()

			return cursor.lastrowid
		except:
			print(sys.exc_info()[0])
			print(sys.exc_info()[1])
			if not self.Continue:
				return 0
			self.Init()
			return self.insert(sql)

	def update(self,sql):
		try:
			cursor = self.cnx.cursor(buffered=True)
			cursor.execute(sql)
			self.cnx.commit()
			return True
		except:
			print(sys.exc_info()[0])
			print(sys.exc_info()[1])
			if not self.Continue:
				return 0
			self.Init()
			return self.update(sql)

	def remove(self,sql):
		try:
			cursor = self.cnx.cursor(buffered=True)
			cursor.execute(sql)
			self.cnx.commit()
			return True
		except:
			print(sys.exc_info()[0])
			print(sys.exc_info()[1])
			return False
global db
db = Database()
