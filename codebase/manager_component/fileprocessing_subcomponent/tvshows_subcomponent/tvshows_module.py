from . import tvshows_class as TVShowsClass


# =========================================================================================
# Creates the Library object, which contains file server connectivity data,
# as well as lists of tv shows, and processes copy actions
# =========================================================================================

def createtvshows():
	return TVShowsClass.DefineTVShows()


