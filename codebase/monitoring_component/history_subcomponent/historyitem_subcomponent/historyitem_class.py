


# This class creates an object which is used to capture tracker information about an individual torrent
# The object contains remotely read Deluge Daemon data and presents it in a Download-Manager friendly format


class DefineItem:

	def __init__(self, datetime, sessiondata, vpnstatus):

		self.datetime = datetime
		self.uploaded = sessiondata['uploadedtotal']
		self.red = sessiondata['redcount']
		self.orange = sessiondata['orangecount']
		self.amber = sessiondata['ambercount']
		self.yellow = sessiondata['yellowcount']
		self.green = sessiondata['greencount']
		self.vpnstatus = vpnstatus


	def getdatetime(self):

		return self.datetime

	def getuploaded(self):

		return self.uploaded

	def getvpnstatus(self):

		return self.vpnstatus

	def getsavedata(self):

		outcome = self.datetime.getiso() + "|" + str(self.uploaded) + "|" + str(self.green) + "|"
		outcome = outcome + str(self.yellow) + "|" + str(self.amber) + "|" + str(self.orange) + "|"
		outcome = outcome + str(self.red) + "|" + str(self.vpnstatus)
		return outcome

	def getgraphdata(self):

		outcome = []
		if self.red > 0:
			for index in range(0, self.red):
				outcome.append("red")
		if self.orange > 0:
			for index in range(0, self.orange):
				outcome.append("orange")
		if self.amber > 0:
			for index in range(0, self.amber):
				outcome.append("amber")
		if self.yellow > 0:
			for index in range(0, self.yellow):
				outcome.append("yellow")
		if self.green > 0:
			for index in range(0, self.green):
				outcome.append("green")
		return outcome


	def cumulate(self, anotherhistoryitem):

		self.uploaded = max(anotherhistoryitem.uploaded, self.uploaded)
		self.red = self.red + anotherhistoryitem.red
		self.orange = self.orange + anotherhistoryitem.orange
		self.amber = self.amber + anotherhistoryitem.amber
		self.yellow = self.yellow + anotherhistoryitem.yellow
		self.green = self.green + anotherhistoryitem.green
		if anotherhistoryitem.vpnstatus != 1:
			self.vpnstatus = 0



	def getlonggraphdata(self):

		sessiondata = {}
		sessiondata['red'] = self.red
		sessiondata['orange'] = self.orange
		sessiondata['amber'] = self.amber
		sessiondata['yellow'] = self.yellow
		sessiondata['green'] = self.green
		return sessiondata

