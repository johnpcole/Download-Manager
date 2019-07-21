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
			newinstruction = self.scraper.getwebresult()
			print("====================================")
			print("=====instruction from manager=======")
			print(newinstruction)
			print("====================================")
			if CopyInstruction.isvalidinstruction(newinstruction) == True:
				if CopyInstruction.isalldone(newinstruction['copyid']) == True:
					longwait = self.performafinish()
				else:
					if CopyInstruction.isfolderrefresh(newinstruction['copyid']) == True:
						self.performafolderrefresh()
					else:
						self.performacopy(newinstruction['copyid'], newinstruction['source'],
														newinstruction['target'], newinstruction['overwrite'])
			else:
				print("Invalid response from Download-Manager")

		if longwait == True:
			self.delayer.waitlong()
		else:
			self.delayer.waitshort()



	def performafolderrefresh(self):
		self.lastinstruction.setrefreshfolders()
		copyoutcome = self.filemanager.scrapetvshows()
		self.lastinstruction.updatenotes(copyoutcome)



	def performafinish(self):
		longwait = False
		self.filemanager.disconnectfileserver()
		if self.lastinstruction.isalldone() == True:
			longwait = True
		self.lastinstruction.setalldone()
		return longwait


	def performacopy(self, copyid, source, target, forcemode):
		self.lastinstruction.settonew(copyid)
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




