from . import historyitem_class as HistoryItemClass
from ...common_components.datetime_datatypes import datetime_module as DateTime


def createhistoryitem(datetime, sessiondata, vpnstatus):
	return HistoryItemClass.DefineItem(datetime, sessiondata, vpnstatus)



def createfromfile(monitordata):
	dataarray = monitordata.split("|")
	sessiondata = {}
	sessiondata['uploadedtotal'] = int(dataarray[1])
	sessiondata['redcount'] = int(dataarray[6])
	sessiondata['orangecount'] = int(dataarray[5])
	sessiondata['ambercount'] = int(dataarray[4])
	sessiondata['yellowcount'] = int(dataarray[3])
	sessiondata['greencount'] = int(dataarray[2])
	if len(dataarray) > 7:
		vpnstatus = dataarray[7]
	else:
		vpnstatus = False
	return HistoryItemClass.DefineItem(DateTime.createfromiso(dataarray[0]), sessiondata, vpnstatus)


