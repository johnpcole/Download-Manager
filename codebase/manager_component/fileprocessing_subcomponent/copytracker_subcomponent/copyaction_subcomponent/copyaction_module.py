from . import copyaction_class as CopyActionClass


def createcopyaction(source, target, torrentid, torrentname):
	return CopyActionClass.DefineActionItem(source, target, torrentid, torrentname)

def createblankcopyaction():
	return CopyActionClass.DefineActionItem("", "", "< IGNORE >", "")
