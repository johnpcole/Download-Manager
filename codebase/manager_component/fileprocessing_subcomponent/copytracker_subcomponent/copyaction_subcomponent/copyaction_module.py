from . import copyaction_class as CopyActionClass


def createcopyaction(source, target, torrentid):
	return CopyActionClass.DefineActionItem(source, target, torrentid)

def createblankcopyaction():
	return CopyActionClass.DefineActionItem("", "", "")
