import mysql.connector
import sys
from mysql.connector import errorcode

sys.dont_write_bytecode = True

class MySQLConnector():

	##
	# Construct MySQLConnector class
	# If host and user parameters are given, it will attempt to create a connection to MySQL at initialization.
	#
	# @param host MySQL server host.
	# @param user Username to connect to MySQL server.
	# @param password Password to connect to MySQL server.
	# @param schema Schema to connect to in MySQL server.
	# @param port Port that MySQL server is listening for connection requests on.
	#
	def __init__(self, password, host=None, user=None, schema=None, port=None):
		if host is not None and user is not None:
			if port is None:
				try:
					self.conn = mysql.connector.connect(host=host, user=user, password=password, buffered=True)
					self.cursor = self.conn.cursor()
				except mysql.connector.Error as err:
					if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
						print "Something is wrong with given user name or password."
					elif err.errno == errorcode.ER_BAD_DB_ERROR:
						print "Database does not exist."
					else:
						print err
			elif port is not None:
				try:
					self.conn = mysql.connector.connect(host=host, user=user, password=password, database=schema, port=port, buffered=True)
					self.cursor = self.conn.cursor()
				except mysql.connector.Error as err:
					if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
						print "Something is wrong with given user name or password."
					elif err.errno == errorcode.ER_BAD_DB_ERROR:
						print "Database does not exist."
					else:
						print err
			if schema is not None:
				self.cursor.execute("CREATE DATABASE IF NOT EXISTS {0}".format(schema))
				self.cursor.execute("USE {0}".format(schema))
	##
	# Connect to MySQL
	#
	# @param host MySQL server host.
	# @param user Username to connect to MySQL server.
	# @param password Password to connect to MySQL server.
	# @param schema Schema to connect to in MySQL server - Will be created if it does not exist.
	# @param port Port that MySQL server is listening for connection requests on.
	#
	def mysql_connect(self, host, user, password, schema=None, port=None):
		# Close connection before switching to another MySQL server
		self.conn.close()
		try:
			if port is None:
				self.conn = mysql.connector.connect(host=host, user=user, password=password, buffered=True)
				self.cursor = self.conn.cursor()
			elif port is not None:
				self.conn = mysql.connector.connect(host=host, user=user, password=password, port=port, buffered=True)
				self.cursor = self.conn.cursor()
			if schema is not None:
				self.cursor.execute("CREATE DATABASE IF NOT EXISTS {0}".format(schema))
				self.cursor.execute("USE {0}".format(schema))
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print "Something is wrong with specified user name or password"
			else:
				print (err)

	##
	# Process SQL query
	#
	# @param sql SQL query.
	# @param arguments Arguments for SQL query
	#
	def mysql_query(self, sql, arguments=None):
		try:
			#self.conn.autocommit = False
			if arguments is None:
				self.cursor.execute(sql)
			elif arguments is not None:
				self.cursor.executemany(sql,arguments)
			self.conn.commit()
			self.conn.autocommit = True
			fields = self.cursor.fetchall()
			return fields
		except mysql.connector.InterfaceError:
			pass
		except mysql.connector.DatabaseError as err:
			if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
				pass
			raise
		except:
			raise

	##
	# Disconnect from MySQL
	#
	def mysql_disconnect(self):
		try:
			self.conn.close()
		except mysql.connector.Error as err:
			print err
