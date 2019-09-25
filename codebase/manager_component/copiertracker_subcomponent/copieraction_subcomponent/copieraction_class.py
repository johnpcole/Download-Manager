from ....common_components.enumeration_datatype import enumeration_module as Enumeration
from . import copieraction_privatefunctions as Functions

class DefineCopierActionItem:

	def __init__(self, actiontype, source, target, torrentid, torrentname):


		self.actiontype = Enumeration.createenum(["Copy File", "Scrape TV Shows"], actiontype)

		self.source = source

		self.target = target

		self.status = Enumeration.createenum(["Queued", "In Progress", "Failed", "Succeeded", "Confirm", "Abandoned"],
																											"Queued")
		self.resultdetail = {}

		self.torrentid = torrentid

		self.torrentname = torrentname

		self.cacheupdateflag = False

		self.forcecopy = False

# =========================================================================================

	def getcachestate(self):

		return self.cacheupdateflag

# =========================================================================================

	def updatestatusandresultdetail(self, newstatus, newresultdetail):

		self.cacheupdateflag = True
		self.resultdetail = newresultdetail
		self.status.set(newstatus)

# =========================================================================================

	def intervention(self, intervention):

		self.cacheupdateflag = True
		if intervention == "Abandon":
			if (self.status.get("Failed") == True) or (self.status.get("Confirm") == True):
				self.status.set("Abandoned")
			else:
				print("Invalid Abandon intervention for status ",self.status.displaycurrent())
		elif intervention == "Overwrite":
			if self.status.get("Confirm") == True:
				self.status.set("Queued")
				self.forcecopy = True
			else:
				print("Invalid Overwrite intervention for status ", self.status.displaycurrent())
		elif intervention == "Retry":
			if self.status.get("Failed") == True:
				self.status.set("Queued")
			else:
				print("Invalid Retry intervention for status ",self.status.displaycurrent())
		else:
			print("Unknown intervention specified: ", intervention)

# =========================================================================================

	def getactiontype(self):

		return self.actiontype.displaycurrent()

# =========================================================================================

	def getstatus(self):

		return self.status.displaycurrent()

# =========================================================================================

	def gettorrentid(self):

		return self.torrentid


# =========================================================================================

	def isvalidscrapedata(self):

		outcome = False
		if self.actiontype.get("Scrape TV Shows") == True:
			if self.status.get("Succeeded") == True:
				outcome = True

		return outcome

# =========================================================================================

	def getcopieractioninstruction(self, nextactionid):

		outcome = {'action': self.actiontype.displaycurrent(),
					'copyid': nextactionid}
		if self.actiontype.get("Copy File") == True:
			outcome['source'] = self.source
			outcome['target'] = self.target
			outcome['overwrite'] = self.forcecopy
		return outcome

# =========================================================================================

	def getcopierpageloaddata(self, torrentidlist, actionid):

		outcome = {'action': self.actiontype.displaycurrent(),
					'status': Functions.sanitisestatus(self.status.displaycurrent()),
					'copyid': actionid,
					'datetimestamp': Functions.sanitisecopydatetimestamp(actionid)}

		if self.actiontype.get("Copy File") == True:
			outcome['target'] = Functions.sanitisetargetpath(self.target)
			outcome['source'] = self.source
			outcome['torrentid'] = self.torrentid
			#outcome['result'] = Functions.rendercopyresults(self.resultdetail, self.status)
			outcome['torrentname'] = self.torrentname
			if self.torrentid in torrentidlist:
				outcome['stillavailable'] = "Yes"
			else:
				outcome['stillavailable'] = "No"
		else:
			outcome['target'] = "Search the Videos drive for TV Shows & their Seasons"
			outcome['source'] = ""
			outcome['torrentid'] = ""
			#outcome['result'] = ['TV Shows Found' + str(len(self.resultdetail))]
			outcome['torrentname'] = "Adds newly created TV Show & Season folders on the Video drive to the TV Show options lists"
			outcome['stillavailable'] = "Yes"

		self.cacheupdateflag = False
		return outcome


# =========================================================================================

	def getcopierpageupdatedata(self, actionid):

		statuslabel = Functions.sanitisestatus(self.status.displaycurrent())
		self.cacheupdateflag = False
		return {'status': statuslabel, 'result': self.resultdetail, 'copyid': actionid}

# =========================================================================================

	def getcopieractiondetail(self):

		if self.actiontype.get("Copy File") == True:
			outcome = Functions.rendercopyresults(self.resultdetail, self.status, self.target)
		else:
			dummydata = [["", ""], ["", ""]]
			outcome = {"filepath": str(len(self.resultdetail)) + ' TV Shows Found',
																			"outcomes": dummydata, "description": ""}
		return outcome




