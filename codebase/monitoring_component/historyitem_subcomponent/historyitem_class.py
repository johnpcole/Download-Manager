from . import historyitem_privatefunctions as Functions



# This class creates an object which is used to capture tracker information about an individual torrent
# The object contains remotely read Deluge Daemon data and presents it in a Download-Manager friendly format


class DefineItem:

	def __init__(self, datetime, sessiondata):

		self.datetime = datetime
		self.uploaded = sessiondata['uploadedtotal']
		self.red = sessiondata['redcount']
		self.orange = sessiondata['orangecount']
		self.amber = sessiondata['ambercount']
		self.yellow = sessiondata['yellowcount']
		self.green = sessiondata['greencount']



	def getdatetime(self):

		return self.datetime



	def getalldata(self):

		outcome = {}
		outcome['datetime'] = self.datetime.getiso()
		outcome['uploaded'] = self.uploaded
		outcome['red'] = self.red
		outcome['orange'] = self.orange
		outcome['amber'] = self.amber
		outcome['yellow'] = self.yellow
		outcome['green'] = self.green
		return outcome



	def getsavedata(self):

		outcome = self.datetime.getiso() + "|" + str(self.uploaded) + "|" + str(self.green) + "|"
		outcome = outcome + str(self.yellow) + "|" + str(self.amber) + "|" + str(self.orange) + "|" + str(self.red)
		return outcome



	def getgraphicdata(self, horizontaloffset, verticaloffset, boxwidth, boxheight, origintimeobject):

		outcome = []
		ver = verticaloffset
		horizontalinstruction = Functions.geteradifference(origintimeobject, self.datetime)
		print("====================================================")
		print(origintimeobject.getiso(), self.datetime.getiso(), horizontaloffset)
		print("====================================================")
		if horizontalinstruction > -1:
			hor = horizontaloffset + ((horizontalinstruction + 1) * boxwidth)
			#colourlist = {"1#CC0000": self.red, "2#FF6600": self.orange, "3#FFBB11": self.amber, "4#EEEE11": self.yellow, "5#00CC00": self.green}
			colourlist = {"1#CC0000": 4, "2#FF6600": 4, "3#FFBB11": 4, "4#EEEE11": 4, "5#00CC00": 4}
			for colour in sorted(colourlist.keys()):
				if colourlist[colour] > 0:
					for indexer in range(0, colourlist[colour]):
						instruction = 'fill="' + colour[1:] + '" ' + 'x="' + str(hor) + '" y="' + str(ver)
						instruction = instruction + '" width="' + str(boxwidth) + '" height="' + str(boxheight) + '"'
						if ver > 5:
							outcome.append(instruction)
							ver = ver - boxheight - 1

		return outcome
