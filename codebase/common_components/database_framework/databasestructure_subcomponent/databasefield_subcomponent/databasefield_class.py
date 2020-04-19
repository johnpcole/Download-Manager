class DefineDatabaseField:

	def __init__(self, tablename, fieldname, fieldtype, nullable, primarykey):

		self.tablename = tablename

		self.fieldname = fieldname

		self.fieldtype = fieldtype

		self.nullable = nullable

		self.primarykey = primarykey


	def gettablename(self):

		return self.tablename

	def getfieldname(self):

		return self.fieldname

	def getfieldcreationsql(self):

		outcome = self.fieldname + " " + self.fieldtype
		if self.primarykey is True:
			outcome = outcome + " PRIMARY KEY"
		if self.nullable is False:
			outcome = outcome + " NOT NULL"

		return outcome



