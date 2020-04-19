from .databasefield_subcomponent import databasefield_module as FieldClass


class DefineDatabaseStructure:

	def __init__(self):

		self.fieldslist = []



	def adddatabasestructure(self, tablename, fieldname, fieldtype, nullable, primarykey, databasemode):

		if databasemode.get('Build') is True:

			# Ought to put in a duplicate check

			self.fieldslist.append(FieldClass.createdatabasefield(tablename, fieldname, fieldtype, nullable, primarykey))
		else:
			assert(1 == 0, "Attempting to alter database structure while database is Live")



	def gettablelist(self):

		outcome = []
		for fielddef in self.fieldslist:
			tablename = fielddef.gettablename()
			if tablename not in outcome:
				outcome.append(tablename)
		return outcome



	def gettablefields(self, desiredtablename):

		outcome = []
		for fielddef in self.fieldslist:
			tablename = fielddef.gettablename()
			if tablename == desiredtablename:
				outcome.append(fielddef)
		return outcome



	def gettablecreationsql(self, tablename):

		sqlcommand = ""
		columndefinitionlist = self.gettablefields(tablename)
		for columndefinition in columndefinitionlist:
			if sqlcommand != "":
				sqlcommand = sqlcommand + ", "
			sqlcommand = sqlcommand + columndefinition.getfieldcreationsql()
		sqlcommand = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + sqlcommand + ");"
		return sqlcommand




