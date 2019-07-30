from . import copiertracker_class as CopierTrackerClass


# =========================================================================================
# Creates the Library object, which contains file server connectivity data,
# as well as lists of tv shows, and processes copy actions
# =========================================================================================

def createtracker():
	return CopierTrackerClass.DefineCopierTracker()

