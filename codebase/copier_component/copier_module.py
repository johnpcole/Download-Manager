from . import copier_class as CopierClass

def createcopier(webaddress, erasize, retrylimit):

	return CopierClass.DefineCopier(webaddress, erasize, retrylimit)

