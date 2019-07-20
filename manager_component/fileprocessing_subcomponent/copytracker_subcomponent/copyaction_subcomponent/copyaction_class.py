from .....common_components.enumeration_datatype import enumeration_module as Enumeration
from .....common_components.datetime_datatypes import datetime_module as DateTime


class DefineActionItem:

	def __init__(self, source, target, index, torrentid):

		self.source = source

		self.target = target

		self.status = Enumeration.createenum(["Queued", "In Progress", "Failed", "Succeeded", "Confirm"], "Queued")

		currentdatetime = DateTime.getnow()
		indexstring = "0000" + str(index % 1000)
		self.index = currentdatetime.getiso() + indexstring[-3:]

		self.torrentid = torrentid


# =========================================================================================

	def updatestatus(self, newstatus):

		return self.status.set(newstatus)

# =========================================================================================

	def confirmstatus(self, statuscheck):

		return self.status.get(statuscheck)

# =========================================================================================

	def getstatus(self):

		return self.status.displaycurrent()

# =========================================================================================

	def getsource(self):

		return self.source

# =========================================================================================

	def gettarget(self):

		return self.target

# =========================================================================================

	def getid(self):

		return self.index


