from . import file_class as FileClass


def createfile(fileid, path, size):
	return FileClass.DefineFile(fileid, path, size)

