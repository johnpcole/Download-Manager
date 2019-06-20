from . import webscraper_class as WebScraperClass


def createscraper(webpageurl):
	return WebScraperClass.DefineScraper(webpageurl)

