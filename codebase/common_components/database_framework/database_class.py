from .databasestructure_subcomponent import databasestructure_module as DatabaseStructure
from .databaseconnection_subcomponent import databaseconnection_module as DatabaseConnection
from . import database_privatefunctions as Function
from ..enumeration_datatype import enumeration_module as Enumeration


class DefineDatabase:

	def __init__(self, databasefilename, turn):

		self.databasestructure = DatabaseStructure.createdatabasestructure()

		self.databaseconnection = DatabaseConnection.createdatabaseconnection(databasefilename, turn)

		self.databasemode = Enumeration.createenum(['Build', 'Live'], 'Build')



	def adddatabasestructure(self, tablename, fieldname, fieldtype, nullable, primarykey):

		self.databasestructure.adddatabasestructure(tablename, fieldname, fieldtype, nullable, primarykey, self.databasemode)



	def changedatabasestate(self, newstate):

		self.databasemode.set(newstate)





	def createentiredatabase(self):

		tablelist = self.databasestructure.gettablelist()
		for tablename in tablelist:
			self.createdatabasetable(tablename)



	def createdatabasetable(self, tablename):

		sqlcommand = self.databasestructure.gettablecreationsql(tablename)
		self.databaseconnection.performdatabaseoperation(sqlcommand, None, self.databasemode)



	def deletedatabaserows(self, deletingrows):

		for databaseoperation in deletingrows:

			sqlcommand = "DELETE FROM " + databaseoperation['recordtype']
			sqlcommand = sqlcommand + Function.buildwheresql(databaseoperation) + ";"
			valuelist = Function.buildvaluessql(databaseoperation)

			self.databaseconnection.performdatabaseoperation(sqlcommand, tuple(valuelist), self.databasemode)



	def insertdatabaserows(self, newrows):

		for databaseoperation in newrows:

			sqlcommand = "INSERT INTO " + databaseoperation['recordtype']
			sqlcommand = sqlcommand + " (" + Function.buildfieldssql(databaseoperation, ", ", False) + ")"
			sqlcommand = sqlcommand + Function.buildparameterssql(databaseoperation) + ";"
			valuelist = Function.buildvaluessql(databaseoperation)

			self.databaseconnection.performdatabaseoperation(sqlcommand, tuple(valuelist), self.databasemode)



	def extractdatabaserows(self, lookuprows):

		outcome = []

		for databaseoperation in lookuprows:

			databasetable = databaseoperation['recordtype']
			databasefields = self.databasestructure.gettablefields(databasetable)
			sqlcommand = "SELECT " + Function.buildfieldnamelistsql(databasefields)
			sqlcommand = sqlcommand + " FROM " + databasetable
			sqlcommand = sqlcommand + Function.buildwheresql(databaseoperation) + ";"
			valuelist = Function.buildvaluessql(databaseoperation)

			lookupdata = self.databaseconnection.performdatabaseextract(sqlcommand, tuple(valuelist), self.databasemode)

			for lookupitem in lookupdata:

				newitem = Function.buildresult(databasefields, lookupitem)
				newitem['recordtype'] = databasetable
				#print(newitem)
				outcome.append(newitem)

		return outcome


