from deluge_client import DelugeRPCClient as DelugeDaemonInterface

# This class creates an object which is used to interface to a Deluge Daemon (via the RPCClient)
# The object doesn't store any useful information itself, but present the most useful torrent management functions
# via simple commands, without having to know RPCClient call names or data keys


class DefineDelugeInterface:

	def __init__(self, address, port, username, password):

		# The actual interface with the deluge daemon, via the RPCClient package
		# This object captures the interface (including address & credentials) to be
		# opened, closed, and used to pass messages to the daemon
		self.delugeinterface = DelugeDaemonInterface(address, port, username, password)

		# The deluge keys used for gaining overall session data via the 'core.get_session_status' call
		self.delugekeysforsessioninfo = ["payload_download_rate", "payload_upload_rate"]

		# The deluge keys used for gaining detailed data about a single torrent via the 'core.get_torrent_status' call
		self.delugekeysfortorrentinfo = ["state", "save_path", "name", "total_size", "progress", "eta",
												"files", "is_finished", "time_added", "num_seeds", "num_peers"]

		# The full list deluge keys available for gaining detailed data about a single torrent via the
		# 'core.get_torrent_status' call
		self.alldelugekeysavailablefortorrentinfo = ["state", "save_path", "tracker", "tracker_status", "next_announce",
														"name", "total_size", "progress", "num_seeds", "total_seeds",
														"num_peers", "total_peers", "eta", "download_payload_rate",
														"upload_payload_rate", "ratio", "distributed_copies",
														"num_pieces", "piece_length", "total_done", "files",
														"file_priorities", "file_progress", "peers", "is_seed",
														"is_finished", "active_time", "seeding_time"]



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
# Returns a structured/layered dictionary of information about a specified (by GUID) torrent
# =========================================================================================

	def gettorrentdata(self, torrentid):

		rawtorrentdata = self.delugeinterface.call('core.get_torrent_status', torrentid, self.delugekeysfortorrentinfo)

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
# Adds a new torrent to the daemon, using the specified link URL
# Returns the GUID of the added torrent
# =========================================================================================

	def addtorrentlink(self, linkstring):

		if linkstring[:7] == "magnet:":
			outcome = self.delugeinterface.call('core.add_torrent_magnet', linkstring, {})
		else:
			outcome = self.delugeinterface.call('core.add_torrent_url', linkstring, {})

		return outcome.decode("ascii", "ignore")



# =========================================================================================
# Instigates a recheck of the specified (by GUID) torrent
# (Returns the RPCClient response, an unknown object)
# =========================================================================================

	def rechecktorrent(self, torrentids):

		return self.delugeinterface.call('core.force_recheck', torrentids)



# =========================================================================================
# Pauses the specified (by GUID) torrent
# If "ALL" is specified, all torrents in the daemon are paused
# (Returns the RPCClient response, an unknown object)
# =========================================================================================

	def pausetorrent(self, torrentid):

		if torrentid == "ALL":
			outcome = self.delugeinterface.call('core.pause_all_torrents')
		else:
			outcome = self.delugeinterface.call('core.pause_torrent', [torrentid])
		return outcome



# =========================================================================================
# Unpauses the specified (by GUID) torrent
# If "ALL" is specified, all torrents in the daemon are unpaused
# (Returns the RPCClient response, an unknown object)
# =========================================================================================

	def resumetorrent(self, torrentid):

		if torrentid == "ALL":
			outcome = self.delugeinterface.call('core.resume_all_torrents')
		else:
			outcome = self.delugeinterface.call('core.resume_torrent', [torrentid])
		return outcome



# =========================================================================================
# Deletes the specified (by GUID) torrent
# (Returns the RPCClient response, an unknown object)
# =========================================================================================

	def deletetorrent(self, torrentid):

		return self.delugeinterface.call('core.remove_torrent', torrentid, True)



# =========================================================================================
# Returns a dictionary of information about the daemon session
# =========================================================================================

	def getsessiondata(self):

		rawstats1 = self.delugeinterface.call('core.get_session_status', self.delugekeysforsessioninfo)
		rawstats2 = self.delugeinterface.call('core.get_free_space')

		outcome = {}
		outcome['uploadspeed'] = rawstats1[b'payload_upload_rate']
		outcome['downloadspeed'] = rawstats1[b'payload_download_rate']
		outcome['freespace'] = rawstats2 / 1000000000
		return outcome
