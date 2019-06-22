from . import historyitem_class as HistoryItemClass
from ...common_components.datetime_datatypes import datetime_module as DateTime


def createhistoryitem(datetime, sessiondata, vpnstatus):
	if vpnstatus == True:
		vs = 1
	else:
		vs = 0

	return HistoryItemClass.DefineItem(datetime, sessiondata, vs)



def createfromfile(monitordata):
	dataarray = monitordata.split("|")
	sessiondata = {}
	sessiondata['uploadedtotal'] = int(dataarray[1])
	sessiondata['redcount'] = int(dataarray[6])
	sessiondata['orangecount'] = int(dataarray[5])
	sessiondata['ambercount'] = int(dataarray[4])
	sessiondata['yellowcount'] = int(dataarray[3])
	sessiondata['greencount'] = int(dataarray[2])
	vs = 0
	if len(dataarray) > 7:
		if dataarray == "1":
			vs = 1

	return HistoryItemClass.DefineItem(DateTime.createfromiso(dataarray[0]), sessiondata, vs)


