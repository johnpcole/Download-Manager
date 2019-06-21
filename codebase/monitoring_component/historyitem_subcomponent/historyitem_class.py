from ...common_components.datetime_datatypes import eras_module as EraFunctions



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

	def getuploaded(self):

		return self.uploaded



#	def getalldata(self):
#
#		outcome = {}
#		outcome['datetime'] = self.datetime.getiso()
#		outcome['uploaded'] = self.uploaded
#		outcome['red'] = self.red
#		outcome['orange'] = self.orange
#		outcome['amber'] = self.amber
#		outcome['yellow'] = self.yellow
#		outcome['green'] = self.green
#		return outcome



	def getsavedata(self):

		outcome = self.datetime.getiso() + "|" + str(self.uploaded) + "|" + str(self.green) + "|"
		outcome = outcome + str(self.yellow) + "|" + str(self.amber) + "|" + str(self.orange) + "|" + str(self.red)
		return outcome



	def getstatusgraphicdata(self, horizontaloffset, verticaloffset, boxwidth, boxheight, origintimeobject, erasize):

		outcome = []
		ver = verticaloffset
		horizontalinstruction = EraFunctions.geteradifference(origintimeobject, self.datetime, erasize)
		if horizontalinstruction > 0:
			hor = horizontaloffset + (horizontalinstruction * (boxwidth + 1))
			colourlist = {"1#CC0000": self.red, "2#FF6600": self.orange, "3#FFBB11": self.amber, "4#EEEE11": self.yellow, "5#00CC00": self.green}
			#colourlist = {"1#CC0000": 4, "2#FF6600": 4, "3#FFBB11": 4, "4#EEEE11": 4, "5#00CC00": 4}
			for colour in sorted(colourlist.keys()):
				if colourlist[colour] > 0:
					for indexer in range(0, colourlist[colour]):
						instruction = 'fill="' + colour[1:] + '" ' + 'x="' + str(hor) + '" y="' + str(ver)
						instruction = instruction + '" width="' + str(boxwidth) + '" height="' + str(boxheight) + '"'
						if ver > 5:
							outcome.append(instruction)
							ver = ver - boxheight - 1

		return outcome



	def getuploadgraphicdata(self, horizontaloffset, verticaloffset, boxwidth, baselineuploaded, origintimeobject, erasize):

		outcome = []
		horizontalinstruction = EraFunctions.geteradifference(origintimeobject, self.datetime, erasize)
		if horizontalinstruction > 0:
			boxheight = (125 * (self.uploaded - baselineuploaded)) / 1000000000
			if boxheight > 0.125:
				boxheight = 125
			if boxheight > -1:
				ver = verticaloffset + 260 - boxheight
				hor = horizontaloffset + (horizontalinstruction * (boxwidth + 1))
				instruction = 'x="' + str(hor) + '" y="' + str(ver)
				instruction = instruction + '" width="' + str(boxwidth) + '" height="' + str(boxheight) + '"'
				outcome.append(instruction)

		return outcome
