from .....common_components.enumeration_datatype import enumeration_module as Enumeration
from . import copieraction_privatefunctions as Functions

class DefineCopierActionItem:

	def __init__(self, actiontype, source, target, torrentid, torrentname):


		self.actiontype = Enumeration.createenum(["Copy File", "Scrape TV Shows"], actiontype)

		self.source = source

		self.target = target

		self.status = Enumeration.createenum(["Queued", "In Progress", "Failed", "Succeeded", "Confirm", "Abandoned"],
																											"Queued")
		self.resultdetail = ""

		self.torrentid = torrentid

		self.torrentname = torrentname

		self.cacheupdateflag = False

# =========================================================================================

	def getcachestate(self):

		return self.cacheupdateflag

# =========================================================================================

	def updatestatusandresultdetail(self, newstatus, newresultdetail):

		self.cacheupdateflag = True
		self.resultdetail = newresultdetail
		self.status.set(newstatus)

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

	def getresultdetail(self):

		return self.resultdetail


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
					'copyid': nextactionid,
					'overwrite': False}
		if self.actiontype.get("Copy File") == True:
			outcome['source'] = self.source
			outcome['target'] = self.target

		return outcome

# =========================================================================================

	def getcopierpageloaddata(self, torrentidlist, actionid):

		outcome = {'action': self.actiontype.displaycurrent(),
					'status': Functions.sanitisestatus(self.status.displaycurrent()),
					'result': self.resultdetail,
					'copyid': actionid,
					'datetimestamp': Functions.sanitisecopydatetimestamp(actionid)}

		if self.actiontype.get("Copy File") == True:
			outcome['target'] = Functions.sanitisetargetpath(self.target)
			outcome['source'] = self.source
			outcome['torrentid'] = self.torrentid
			outcome['torrentname'] = self.torrentname
			if self.torrentid in torrentidlist:
				outcome['stillavailable'] = "Yes"
			else:
				outcome['stillavailable'] = "No"
		else:
			outcome['target'] = "Search the Videos drive for TV Shows & their Seasons"
			outcome['source'] = ""
			outcome['torrentid'] = ""
			outcome['torrentname'] = "Includes newly added TV Show & Season folders on the Video drive"
			outcome['stillavailable'] = "Yes"

		self.cacheupdateflag = False
		return outcome


# =========================================================================================

	def getcopierpageupdatedata(self, actionid):

		statuslabel = Functions.sanitisestatus(self.status.displaycurrent())
		self.cacheupdateflag = False
		return {'status': statuslabel, 'result': self.resultdetail, 'copyid': actionid}

# =========================================================================================
