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

		self.latestaction = DateTime.createfromiso("20000101000000")



	def refresh(self):

		newinstruction = self.copieractionqueue.readfromqueue()

		if CopyInstruction.isvalidinstruction(newinstruction) is True:
			self.performanaction(newinstruction)
		else:
			sleeptrigger = DateTime.getnow()
			sleeptrigger.adjustseconds(-10)
			if DateTime.isfirstlaterthansecond(sleeptrigger, self.latestaction) is True:
				self.filemanager.gotosleep()



	def performanaction(self, newinstruction):
		copyid = newinstruction['copyid']
		if CopyInstruction.isfolderrefresh(newinstruction) is True:
			self.begininstruction(copyid, "Scrape TV Shows")
			actionoutcome = self.filemanager.scrapetvshows()
		else:
			self.begininstruction(copyid, "File Copy")
			actionoutcome = self.filemanager.performcopy(newinstruction['source'], newinstruction['target'],
																							newinstruction['overwrite'])

		self.endinstruction(actionoutcome)






	def begininstruction(self, copyid, instructiontype):
		self.lastinstruction.settonew(copyid, instructiontype)
		self.copierdatastream.createqueueditem(self.lastinstruction.getstatus())

	def endinstruction(self, copyoutcome):
		self.lastinstruction.updateresults(copyoutcome["outcome"], copyoutcome["feedback"])
		self.copierdatastream.createqueueditem(self.lastinstruction.getstatus())
		self.latestaction.settonow()


