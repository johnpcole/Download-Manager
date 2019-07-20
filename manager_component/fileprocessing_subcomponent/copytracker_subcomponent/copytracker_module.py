from . import copytracker_class as CopyTrackerClass


# =========================================================================================
# Creates the Library object, which contains file server connectivity data,
# as well as lists of tv shows, and processes copy actions
# =========================================================================================

def createtracker():
	return CopyTrackerClass.DefineCopyTracker()

