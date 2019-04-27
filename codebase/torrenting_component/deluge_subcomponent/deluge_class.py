from deluge_client import DelugeRPCClient as DelugeDaemonInterface


class DefineDelugeInterface:
	def __init__(self, address, port, username, password):

		# The actual interface with the deluge daemon, via the RPCClient package
		# This object captures the interface (including address & credentials) to be
		# opened, closed, and used to pass messages to the daemon
		self.delugeinterface = DelugeDaemonInterface(address, port, username, password)

# =========================================================================================
# Opens a connection with the deluge daemon, for messages to be passed to/from it
# =========================================================================================

	def openconnection(self):

		while self.delugeinterface.connected == False:
			self.delugeinterface.connect()
		# print "========================================================="
		# print self.delugeinterface.call('client.api_methods')
		# print "========================================================="
		# WORKS! print self.delugeinterface.call('core.get_free_space')
		# print "========================================================="
		# WORKS! print self.delugeinterface.call('core.get_config')
		# print "========================================================="
		return self.delugeinterface.connected

# =========================================================================================
# Closes the open connection with the deluge daemon
# =========================================================================================

	def closeconnection(self):

		# while self.delugeinterface.connected == True:
		# self.delugeinterface.disconnect()
		return self.delugeinterface.connected

# =========================================================================================
# Returns a list of strings, one per torrent, providing the GUID of each torrent
# =========================================================================================

	def gettorrentlist(self):

		rawtorrentlist = self.delugeinterface.call('core.get_session_state')

		outcome = []
		for rawtorrentid in rawtorrentlist:
			outcome.append(rawtorrentid.decode("ascii", "ignore"))

		return outcome

	# =========================================================================================

	def gettorrentdata(self, torrentid):

		rawtorrentdata = self.delugeinterface.call('core.get_torrent_status', torrentid, self.getdelugekeys())

		outcome = {}

		for itemkey in rawtorrentdata:
			itemdata = rawtorrentdata[itemkey]
			newkeyname = itemkey.decode("utf-8", "ignore")

			if isinstance(itemdata, bytes) == True:
				outcome[newkeyname] = itemdata.decode("utf-8", "ignore")

			elif isinstance(itemdata, tuple) == True:
				newlist = []
				for subitem in itemdata:
					newsubdictionary = {}
					for subitemkey in subitem:
						newsubitemkey = subitemkey.decode("utf-8", "ignore")
						if isinstance(subitem[subitemkey], bytes) == True:
							newsubitemdata = subitem[subitemkey].decode("utf-8", "ignore")
						else:
							newsubitemdata = subitem[subitemkey]
						newsubdictionary[newsubitemkey] = newsubitemdata
					newlist.append(newsubdictionary)
				outcome[newkeyname] = newlist

			else:
				outcome[newkeyname] = itemdata

		return outcome

	# =========================================================================================

	def getdelugekeys(self):

		return ["state", "save_path", "name", "total_size", "progress", "eta", "files", "is_finished", "time_added",
				"num_seeds", "num_peers"]  # , "total_seeds", "total_peers" ]

	# =========================================================================================

	def getalldelugekeys(self):

		return ["state",
				"save_path",
				"tracker",
				"tracker_status",
				"next_announce",
				"name",
				"total_size",
				"progress",
				"num_seeds",
				"total_seeds",
				"num_peers",
				"total_peers",
				"eta",
				"download_payload_rate",
				"upload_payload_rate",
				"ratio",
				"distributed_copies",
				"num_pieces",
				"piece_length",
				"total_done",
				"files",
				"file_priorities",
				"file_progress",
				"peers",
				"is_seed",
				"is_finished",
				"active_time",
				"seeding_time"]

	# =========================================================================================

	def addtorrentlink(self, linkstring):

		if linkstring[:7] == "magnet:":
			outcome = self.delugeinterface.call('core.add_torrent_magnet', linkstring, {})
		else:
			outcome = self.delugeinterface.call('core.add_torrent_url', linkstring, {})

		return outcome.decode("ascii", "ignore")

	# =========================================================================================

	def rechecktorrent(self, torrentids):

		return self.delugeinterface.call('core.force_recheck', torrentids)

	# =========================================================================================

	def pausetorrent(self, torrentid):

		if torrentid == "ALL":
			outcome = self.delugeinterface.call('core.pause_all_torrents')
		else:
			outcome = self.delugeinterface.call('core.pause_torrent', [torrentid])
		return outcome

	# =========================================================================================

	def resumetorrent(self, torrentid):

		if torrentid == "ALL":
			outcome = self.delugeinterface.call('core.resume_all_torrents')
		else:
			outcome = self.delugeinterface.call('core.resume_torrent', [torrentid])
		return outcome

	# =========================================================================================

	def deletetorrent(self, torrentid):

		outcome = self.delugeinterface.call('core.remove_torrent', torrentid, True)

		return outcome

	# =========================================================================================

	def getsessiondata(self):

		rawstats = self.delugeinterface.call('core.get_session_status', ["payload_download_rate",
																		 "payload_upload_rate"])

		outcome = {}
		outcome['uploadspeed'] = rawstats[b'payload_upload_rate']
		outcome['downloadspeed'] = rawstats[b'payload_download_rate']
		outcome['freespace'] = (self.delugeinterface.call('core.get_free_space')) / 1000000000
		return outcome
