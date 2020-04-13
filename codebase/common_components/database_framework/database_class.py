from sqlite3 import connect as ConnectDatabase


class DefineDatabase:

	def __init__(self, databasefilename):

		self.databasename = databasefilename



	def performdatabaseoperation(self, databaseoperation, operationvariables):

		print("============================================")
		print("============================================")
		print("============================================")

		currentconnection = ConnectDatabase(self.databasename)

		if operationvariables is None:
			print("NEW SQL COMMAND")
			print("============================================")
			print(databaseoperation)
			print("============================================")
			currentconnection.execute(databaseoperation)
		else:
			print("NEW SQL COMMAND WITH PARAMETERS")
			print("============================================")
			print(databaseoperation)
			print("============================================")
			print(operationvariables)
			print("============================================")
			currentconnection.execute(databaseoperation, operationvariables)

		print("============================================")

		currentconnection.commit()

		print("============================================")
		print("============================================")
		print("============================================")

		currentconnection.close()



	def createdatabasetable(self, tablename, columndefinitionlist, primarykey):

		sqlcommand = ""
		for columndefinition in columndefinitionlist:
			if sqlcommand != "":
				sqlcommand = sqlcommand + ", "
			sqlcommand = sqlcommand + columndefinition['name'] + " " + columndefinition['type']
			if columndefinition['name'] == primarykey:
				sqlcommand = sqlcommand + " PRIMARY KEY"
			if columndefinition['nullable'] != True:
				sqlcommand = sqlcommand + " NOT NULL"
		sqlcommand = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + sqlcommand + ");"

		self.performdatabaseoperation(sqlcommand, None)


	def deletedatabaserows(self, deletingrows):

		for databaseoperation in deletingrows:

			sqlcommand = "DELETE FROM " + databaseoperation['recordtype'] + " WHERE "
			valuelist = []

			for fieldname in databaseoperation.keys():
				if fieldname != 'recordtype':
					sqlcommand = sqlcommand + fieldname + " = ?"
					valuelist.append(databaseoperation[fieldname])

			self.performdatabaseoperation(sqlcommand, tuple(valuelist))


	def insertdatabaserows(self, newrows):

		for databaseoperation in newrows:

			sqlcommand = "INSERT INTO " + databaseoperation['recordtype']

			fieldlist = ""
			valuelist = []
			parameterlist = ""

			for fieldname in databaseoperation.keys():
				if fieldname != 'recordtype':
					if fieldlist != "":
						fieldlist = fieldlist + ", "
						parameterlist = parameterlist + ", "
					fieldlist = fieldlist + fieldname
					parameterlist = parameterlist + "?"
					valuelist.append(databaseoperation[fieldname])
			fieldlist = " (" + fieldlist + ")"
			parameterlist = " VALUES (" + parameterlist + ");"
	
			sqlcommand = sqlcommand + fieldlist + parameterlist

			self.performdatabaseoperation(sqlcommand, tuple(valuelist))
