from . import copyaction_class as CopyActionClass


def createcopyaction(source, target, index, torrentid):
	return CopyActionClass.DefineActionItem(source, target, index, torrentid)

