def gettrackerstatus(trackerstatus, torrentstatus):

	if torrentstatus[-6:] == "active":
		if trackerstatus.find(" Announce OK") != -1:
			outcome = 'green'
		elif trackerstatus.find(" Error: ") != -1:
			if trackerstatus.find(" Error: timed out") != -1:
				outcome = 'amber'
			elif trackerstatus.find(" Error: Invalid argument") != -1:
				outcome = 'orange'
			else:
				outcome = 'red'
		else:
			outcome = 'yellow'
	else:
		outcome = 'black'

	return outcome




def getfulltorrentstatus(rawstatus, iscompleted):

	status = rawstatus.lower()
	if status == "queued":
		if iscompleted is True:
			outcome = "seeding_queued"
		else:
			outcome = "downloading_queued"
	elif status == "paused":
		if iscompleted is True:
			outcome = "seeding_paused"
		else:
			outcome = "downloading_paused"
	elif status == "downloading":
		outcome = "downloading_active"
	elif status == "seeding":
		outcome = "seeding_active"
	else:
		outcome = status
		
	return outcome




def getconnectionstatusdata(torrentstatus, activepeers, activeseeders):

	outcome = {'activedownloads': 0, 'activeuploads': 0, 'downloadsavailable': 0, 'uploadsavailable': 0}

	if torrentstatus[-6:] == "active":
		outcome['uploadsavailable'] = 1
		if activepeers > 0:
			outcome['activeuploads'] = 1
		if torrentstatus == "downloading_active":
			outcome['downloadsavailable'] = 1
			if activeseeders > 0:
				outcome['activedownloads'] = 1

	return outcome


