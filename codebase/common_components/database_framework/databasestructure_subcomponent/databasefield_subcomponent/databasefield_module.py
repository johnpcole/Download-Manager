from . import databasefield_class as DatabaseFieldClass


def createdatabasefield(tablename, fieldname, fieldtype, nullable, primarykey):
	return DatabaseFieldClass.DefineDatabaseField(tablename, fieldname, fieldtype, nullable, primarykey)


