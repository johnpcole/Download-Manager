from . import copieraction_class as CopierActionClass


def createcopyaction(source, target, torrentid, torrentname, copierhistorylocation):
	return CopierActionClass.DefineCopierActionItem("Copy File", source, target, torrentid, torrentname,
																						copierhistorylocation, "N/A")

def createscrapeaction(copierhistorylocation):
	return CopierActionClass.DefineCopierActionItem("Scrape TV Shows", "N/A", "N/A", "N/A", "N/A",
																						copierhistorylocation, "N/A")

def loadpreviousaction(copierhistorylocation, existingfilename):
	return CopierActionClass.DefineCopierActionItem("Load Old Data", "Unknown", "Unknown", "Unknown", "Unknown",
																			copierhistorylocation, existingfilename)


