from . import historyitem_class as HistoryItemClass


def createhistoryitem(datetime, sessiondata):
	return HistoryItemClass.DefineItem(datetime, sessiondata)



def createfromfile(monitordata):
	dataarray = monitordata.split("|")
	sessiondata = {}
	sessiondata['uploadedtotal'] = dataarray[1]
	sessiondata['redcount'] = dataarray[6]
	sessiondata['orangecount'] = dataarray[5]
	sessiondata['ambercount'] = dataarray[4]
	sessiondata['yellowcount'] = dataarray[3]
	sessiondata['greencount'] = dataarray[2]
	return HistoryItemClass.DefineItem(dataarray[0], sessiondata)


