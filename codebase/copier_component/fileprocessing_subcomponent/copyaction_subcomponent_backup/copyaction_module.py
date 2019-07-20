from . import copyaction_class as CopyActionClass


def createcopyaction(source, target, size, description):
	return CopyActionClass.DefineActionItem(source, target, size, description)

def createconnectaction():
	return CopyActionClass.DefineActionItem('[CONNECT]', '', 0, 'Connect File Server')

def createdisconnectaction():
	return CopyActionClass.DefineActionItem('[DISCONNECT]', '', 0, 'Disconnect File Server')