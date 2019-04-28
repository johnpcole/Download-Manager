from .meter_subcomponent import meter_module as Meter

# This class creates an object which is used to store overarching information about the Deluge Daemon session and
# the Raspberry Pi hardware (e.g. temperature / free disk space), and present the information in a format useful for
# graphical presentation
# The object only stores information fed to it, rather than looking up the information itself,
# and stores the information within each child meter object, rather than on itself; It's just a collection

class DefineSessionDataMeters:

	def __init__(self):

		# Overall Upload Speed
		self.uploadspeed = Meter.createlogarithmicmeter(1.0, "Short")

		# Overall Download Speed
		self.downloadspeed = Meter.createlogarithmicmeter(1.0, "Long")

		# Free space on the disk of the daemon's COMPLETED folder
		self.freespace = Meter.createlogarithmicmeter(3.0, "Long")

		# Temperature of the Raspberry Pi
		self.temperature = Meter.createlinearmeter(32.5, 52.5, "Long")

		# Total number of incomplete torrents that are unpaused
		self.downloadcount = Meter.createblockmeter("Outer")

		# Number of incomplete torrents that are actively leeching filesegments from peers
		self.activedownloads = Meter.createblockmeter("Outer")

		# Total number of complete torrents that are unpaused
		self.uploadcount = Meter.createblockmeter("Inner")

		# Number of complete torrents that are actively seeding filesegments to peers
		self.activeuploads = Meter.createblockmeter("Inner")



# =========================================================================================
# Takes the specified dictionary of session stats and specified system temperature
# and stores them in the meter objects for later use
# Also takes the specified dictionary of detailed torrent data,
# and takes a cumulative count of torrents that are unpaused, and are actively seeding/leeching
# storing them in the meter objects for later use
# =========================================================================================

	def updatesessiondata(self, delugesessiondata, temperaturedata, torrentset):

		self.temperature.setmetervalue(temperaturedata)

		for indexkey in delugesessiondata:

			if indexkey == 'uploadspeed':
				self.uploadspeed.setmetervalue(delugesessiondata[indexkey])
			elif indexkey == 'downloadspeed':
				self.downloadspeed.setmetervalue(delugesessiondata[indexkey])
			elif indexkey == 'freespace':
				self.freespace.setmetervalue(delugesessiondata[indexkey])
			else:
				print("Unexepected session data: ", indexkey)

		totaldownloadcounter = 0
		activedownloadcounter = 0
		totaluploadcounter = 0
		activeuploadcounter = 0

		for existingtorrent in torrentset:

			newcount = existingtorrent.getconnectiondata()

			for indexkey in newcount:
				if indexkey == 'downloadcount':
					totaldownloadcounter = totaldownloadcounter + newcount[indexkey]
				elif indexkey == 'activedownloads':
					activedownloadcounter = activedownloadcounter + newcount[indexkey]
				elif indexkey == 'uploadcount':
					totaluploadcounter = totaluploadcounter + newcount[indexkey]
				elif indexkey == 'activeuploads':
					activeuploadcounter = activeuploadcounter + newcount[indexkey]
				else:
					print("Unexpected torrent data: ", indexkey)

		self.downloadcount.setmetervalue(totaldownloadcounter)
		self.activedownloads.setmetervalue(activedownloadcounter)
		self.uploadcount.setmetervalue(totaluploadcounter)
		self.activeuploads.setmetervalue(activeuploadcounter)




			# =========================================================================================
# Returns a dictionary of dictionaries, which contain the graphical coordinates
# required to draw the meter graphs
# =========================================================================================

	def getstats(self):

		outcome = {}
		outcome['downloadspeed'] = self.downloadspeed.getmeterdata()
		outcome['uploadspeed'] = self.uploadspeed.getmeterdata()
		outcome['space'] = self.freespace.getmeterdata()
		outcome['temperature'] = self.temperature.getmeterdata()
		outcome['downloadcount'] = self.downloadcount.getmeterdata()
		outcome['activedownloads'] = self.activedownloads.getmeterdata()
		outcome['uploadcount'] = self.uploadcount.getmeterdata()
		outcome['activeuploads'] = self.activeuploads.getmeterdata()

#		index = 30.0
#		for indexcounter in range(1, 11):
#			index = index + 2.5
#			item = Functions.getmeterdata(Functions.getlinmeterangle(index, 32.5, 56.25), 0.7, 0.0)
#			dummyoutcome = '                    <line y1="' + str(item['vo']) + '" x1="' + str(item['ho']) + '" y2="' + str(item['vf']) + '" x2="' + str(item['hf']) + '" />'
#			print(dummyoutcome)

		return outcome


