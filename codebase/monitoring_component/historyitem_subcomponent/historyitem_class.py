


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



	def getgraphicdata(self, horizontaloffset, verticaloffset, blockwidth, blockheight):

		outcome = []
		totalheight = verticaloffset
		#colourlist = {"#FF0000": self.red, "#FF6600": self.orange, "#FFAA00": self.amber, "#FFFF00": self.yellow, "#00FF00": self.green}
		colourlist = {"1#CC0000": 4, "2#FF7722": 4, "3#EEAA00": 4, "4#EEEE11": 4, "5#00DD00": 4}
		for colour in sorted(colourlist.keys()):
			if colourlist[colour] > 0:
				for indexer in range(0, colourlist[colour]):
					instruction = 'fill="' + colour[1:] + '" ' + 'x="' + str(horizontaloffset) + '" y="' + str(totalheight)
					instruction = instruction + '" width="' + str(blockwidth) + '" height="' + str(blockheight) + '"'
					outcome.append(instruction)
					totalheight = totalheight - blockheight - 1

		return outcome
