

# This class creates an object which is used to capture tracker information about an individual torrent
# The object contains remotely read Deluge Daemon data and presents it in a Download-Manager friendly format


class DefineItem:

	def __init__(self, datetime, uploadeddelta, redcount, ambercount, greencount):

		self.datetime = datetime

		self.uploadeddelta = uploadeddelta

		self.recount = redcount

		self.ambercount = ambercount

		self.greencount = greencount
