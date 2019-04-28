from . import filedata_class as FileDataClass


def createitem(fileid, path, size):
	return FileDataClass.DefineFileItem(fileid, path, size)

