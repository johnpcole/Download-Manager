from .filemanagement_subcomponent import filemanagement_module as FileManager
from .copyinstruction_subcomponent import copyinstruction_module as CopyInstruction
from ..common_components.filesystem_framework import filesystem_module as FileSystem
from ..common_components.queue_framework import queue_module as Queue
from ..common_components.datetime_datatypes import datetime_module as DateTime


class DefineCopier:

	def __init__(self, copieractionqueuelocation, copierresultslocation, copierappconfiglocation):

		self.filemanager = FileManager.createmanager(FileSystem.readjsonfromdisk(copierappconfiglocation), 3)

		self.lastinstruction = CopyInstruction.createinstruction()

		self.copieractionqueue = Queue.createqueuereader(copieractionqueuelocation)

		self.copierdatastream = Queue.createqueuewriter(copierresultslocation, 24)

		self.latestaction = DateTime.createfromiso("19991231235959")



	def refresh(self):

		newinstruction = self.copieractionqueue.readfromqueue()

		if CopyInstruction.isvalidinstruction(newinstruction) == True:
			self.performanaction(newinstruction)
			self.copierdatastream.createqueueditem(self.lastinstruction.getstatus())
			self.latestaction.settonow()
		else:
			trigger = DateTime.getnow()
			trigger = trigger.adjustseconds(-10)
			if DateTime.isfirstlaterthansecond(trigger, self.latestaction):
				self.performafinish()



	def performanaction(self, newinstruction):
		if CopyInstruction.isfolderrefresh(newinstruction) == True:
			self.performafolderrefresh(newinstruction['copyid'])
		else:
			self.performafilecopy(newinstruction['copyid'], newinstruction['source'],
																newinstruction['target'], newinstruction['overwrite'])



	def performafolderrefresh(self, copyid):
		self.lastinstruction.settonew(copyid, "Scrape TV Shows")
		scrapeoutcome = self.filemanager.scrapetvshows()
		self.lastinstruction.updateresults(scrapeoutcome["outcome"], scrapeoutcome["feedback"])


	def performafinish(self):
		self.filemanager.gotosleep()


	def performafilecopy(self, copyid, source, target, forcemode):
		self.lastinstruction.settonew(copyid, "File Copy")
		copyoutcome = self.filemanager.performcopy(source, target, forcemode)
		self.lastinstruction.updateresults(copyoutcome["outcome"], copyoutcome["feedback"])




