from codebase.common_components.logging_framework import logging_module as Logging
from codebase.common_components.webscraper_framework import webscraper_module as WebScraper
from.codebase.common_components.delayer_framework import delayer_module as Delayer







Logging.printrawline("Starting Download-Manager Application")

delayer = Delayer.createdelayer()
scraper = WebScraper.createscraper("http://127.0.0.1:5000/Monitor")

while 1 != 0:

	if delayer.checkdelay() == True:
		scraper.retrievewebpages(delayer.getlatestcall())
		delayer.waitlong()
	else:
		delayer.waitshort()

Logging.printrawline("Ending Download-Manager Application")

