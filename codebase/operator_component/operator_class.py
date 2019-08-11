from ..common_components.delayer_framework import delayer_module as Delayer
from ..common_components.webscraper_framework import webscraper_module as WebScraper
from .filemanagement_subcomponent import filemanagement_module as FileManager
from .copyinstruction_subcomponent import copyinstruction_module as CopyInstruction

class DefineCopier:

	def __init__(self, webaddress, erasize, retrylimit):

		self.delayer = Delayer.createdelayer(erasize)

		self.scraper = WebScraper.createscraper(webaddress, retrylimit)

		self.filemanager = FileManager.createmanager(FileManager.getlibraryconnectionconfig(), retrylimit)

		self.lastinstruction = CopyInstruction.createinstruction()


	def refresh(self):

		longwait = False

		if self.shouldcalldownloadmanager() == True:
			self.delayer.wait(5)
			self.scraper.posttourl(self.lastinstruction.getstatus())
			newinstruction = self.scraper.getjsonresult()
			if CopyInstruction.isvalidinstruction(newinstruction) == True:
				if CopyInstruction.isalldone(newinstruction) == True:
					longwait = self.performafinish()
				else:
					self.performanaction(newinstruction)

		if longwait == True:
			self.delayer.waitlong()
		else:
			self.delayer.waitshort()


	def performanaction(self, newinstruction):
		if CopyInstruction.isfolderrefresh(newinstruction) == True:
			self.performafolderrefresh(newinstruction['copyid'])
		else:
			self.performafilecopy(newinstruction['copyid'], newinstruction['source'],
							  newinstruction['target'], newinstruction['overwrite'])



	def performafolderrefresh(self, copyid):
		self.lastinstruction.settonew(copyid, "Scrape TV Shows")
		copyoutcome = self.filemanager.scrapetvshows()
		self.lastinstruction.updatenotes(copyoutcome)


	def performafinish(self):
		longwait = False
		self.filemanager.disconnectfileserver()
		if self.lastinstruction.isalldone() == True:
			longwait = True
		self.lastinstruction.setalldone()
		return longwait


	def performafilecopy(self, copyid, source, target, forcemode):
		self.lastinstruction.settonew(copyid, "File Copy")
		copyoutcome = self.filemanager.performcopy(source, target, forcemode)
		self.lastinstruction.updatestatus(copyoutcome)


	def shouldcalldownloadmanager(self):

		calldownloadmanager = False
		if self.lastinstruction.isalldone() == True:
			if self.delayer.checkdelay() == True:
				# If the last instruction was all done, and a minute has elapsed since last time
				calldownloadmanager = True
		else:
			# If the last instruction was a copy don't care how long ago it was
			calldownloadmanager = True

		return calldownloadmanager




