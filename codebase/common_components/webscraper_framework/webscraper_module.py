from . import webscraper_class as WebScraperClass


def createscraper(webpageurl, retrylimit):
	return WebScraperClass.DefineScraper(webpageurl, retrylimit)

