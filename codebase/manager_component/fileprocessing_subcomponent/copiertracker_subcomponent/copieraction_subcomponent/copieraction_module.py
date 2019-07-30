from . import copieraction_class as CopierActionClass


def createcopyaction(source, target, torrentid, torrentname):
	return CopierActionClass.DefineCopierActionItem("Copy File", source, target, torrentid, torrentname)

def createscrapeaction():
	return CopierActionClass.DefineCopierActionItem("Scrape TV Shows", "N/A", "N/A", "N/A", "N/A")

