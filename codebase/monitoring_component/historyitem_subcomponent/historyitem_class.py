


# This class creates an object which is used to capture tracker information about an individual torrent
# The object contains remotely read Deluge Daemon data and presents it in a Download-Manager friendly format


class DefineItem:

	def __init__(self, datetime, sessiondata):

		self.datetime = datetime
		self.uploaded = sessiondata['uploadedtotal']
		self.red = sessiondata['redcount']
		self.amber = sessiondata['ambercount']
		self.green = sessiondata['greencount']



	def getdatetime(self):

		return self.datetime



	def getalldata(self):

		outcome = {}
		outcome['datetime'] = self.datetime.getiso()
		outcome['uploaded'] = self.uploaded
		outcome['red'] = self.red
		outcome['amber'] = self.amber
		outcome['green'] = self.green
		return outcome

