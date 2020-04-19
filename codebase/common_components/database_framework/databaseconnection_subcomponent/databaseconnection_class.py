from sqlite3 import connect as ConnectDatabase


class DefineDatabaseConnection:

	def __init__(self, databasefilename):

		self.databasename = databasefilename

		self.debugging = True



	def performdatabaseextract(self, databaseoperation, operationvariables, databasemode):

		if databasemode.get('Live') is True:

			if self.debugging is True:
				print("============================================")
				print("============================================")
				print("============================================")

			currentconnection = ConnectDatabase(self.databasename)
			currentcursor = currentconnection.cursor()

			if operationvariables is None:

				if self.debugging is True:
					print("NEW SQL CURSOR COMMAND")
					print("============================================")
					print(databaseoperation)
					print("============================================")

				currentcursor.execute(databaseoperation)

			else:

				if self.debugging is True:
					print("NEW SQL CURSOR COMMAND WITH PARAMETERS")
					print("============================================")
					print(databaseoperation)
					print("============================================")
					print(operationvariables)
					print("============================================")

				currentcursor.execute(databaseoperation, operationvariables)

			records = currentcursor.fetchall()

			if self.debugging is True:
				print("============================================")
				print("============================================")
				print("============================================")

			currentcursor.close()
			currentconnection.close()

			return records

		else:
			assert (1 == 0, "Attempting to read database while in build mode")



	def performdatabaseoperation(self, databaseoperation, operationvariables, databasemode):

		if databasemode.get('Live') is True:

			if self.debugging is True:
				print("============================================")
				print("============================================")
				print("============================================")

			currentconnection = ConnectDatabase(self.databasename)

			if operationvariables is None:

				if self.debugging is True:
					print("NEW SQL COMMAND")
					print("============================================")
					print(databaseoperation)
					print("============================================")

				currentconnection.execute(databaseoperation)

			else:

				if self.debugging is True:
					print("NEW SQL COMMAND WITH PARAMETERS")
					print("============================================")
					print(databaseoperation)
					print("============================================")
					print(operationvariables)
					print("============================================")

				currentconnection.execute(databaseoperation, operationvariables)

			if self.debugging is True:
				print("============================================")

			currentconnection.commit()

			if self.debugging is True:
				print("============================================")
				print("============================================")
				print("============================================")

			currentconnection.close()


		else:
			assert (1 == 0, "Attempting to write to database while in build mode")
