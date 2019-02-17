import mysql.connector
import sys
from Shared.Configs import Config

class Database:
	def query(self,sql):
		try:
			cnx = mysql.connector.connect(host=Config.db_host,user=Config.db_user,password=Config.db_password
			,database=Config.databaseName,autocommit=True)
			cursor = cnx.cursor()
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
			return None

	def insert(self,sql):
		try:
			cnx = mysql.connector.connect(host=Config.db_host,user=Config.db_user,password=Config.db_password
			,database=Config.databaseName,autocommit=True)
			cursor = cnx.cursor()
			cursor.execute(sql)
			cnx.commit()

			return cursor.lastrowid
		except:
			print(sys.exc_info()[0])
			print(sys.exc_info()[1])
			return 0

	def update(self,sql):
		try:
			cnx = mysql.connector.connect(host=Config.db_host,user=Config.db_user,password=Config.db_password
			,database=Config.databaseName,autocommit=True)
			cursor = cnx.cursor()
			cursor.execute(sql)
			cnx.commit()
			return True
		except:
			print(sys.exc_info()[0])
			print(sys.exc_info()[1])
			return False

	def remove(self,sql):
		try:
			cnx = mysql.connector.connect(host=Config.db_host,user=Config.db_user,password=Config.db_password
			,database=Config.databaseName,autocommit=True)
			cursor = cnx.cursor()
			cursor.execute(sql)
			cnx.commit()
			return True
		except:
			print(sys.exc_info()[0])
			print(sys.exc_info()[1])
			return False
global db
db = Database()
