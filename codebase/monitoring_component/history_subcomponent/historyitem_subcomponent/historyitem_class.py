


# This class creates an object which is used to capture tracker information about an individual torrent
# The object contains remotely read Deluge Daemon data and presents it in a Download-Manager friendly format


class DefineItem:

	def __init__(self, datetime, uploaded, red, orange, amber, yellow, green, vpnstatus, temperature):

		self.datetime = datetime
		self.uploaded = uploaded
		self.red = red
		self.orange = orange
		self.amber = amber
		self.yellow = yellow
		self.green = green
		self.vpnstatus = vpnstatus
		self.temperature = temperature

	def getdatetime(self):

		return self.datetime

	def getuploaded(self):

		return self.uploaded

	def getvpnstatus(self):

		return self.vpnstatus

	def gettemp(self):

		return self.temperature

	def getsavedata(self):

		outcome = self.datetime.getiso() + "|" + str(self.uploaded) + "|" + str(self.green) + "|"
		outcome = outcome + str(self.yellow) + "|" + str(self.amber) + "|" + str(self.orange) + "|"
		outcome = outcome + str(self.red) + "|" + str(self.vpnstatus) + "|" + str(self.temperature)
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
		self.temperature = max(anotherhistoryitem.temperature, self.temperature)



	def getlonggraphdata(self):

		sessiondata = {}
		sessiondata['red'] = self.red
		sessiondata['orange'] = self.orange
		sessiondata['amber'] = self.amber
		sessiondata['yellow'] = self.yellow
		sessiondata['green'] = self.green
		return sessiondata

