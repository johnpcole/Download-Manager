from . import historyitem_class as HistoryItemClass
from .....common_components.datetime_datatypes import datetime_module as DateTime


def createhistoryitem(datetime, aggregates, vpnstatus, temperature):

	print("====================================")
	print(aggregates)
	print("====================================")
	uploaded = aggregates['uploadedtotal']
	red = aggregates['redcount']
	orange = aggregates['orangecount']
	amber = aggregates['ambercount']
	yellow = aggregates['yellowcount']
	green = aggregates['greencount']

	return HistoryItemClass.DefineItem(datetime, uploaded, red, orange, amber, yellow, green, vpnstatus, temperature)



def createfromfile(monitordata):
	dataarray = monitordata.split("|")
	datetime = DateTime.createfromiso(dataarray[0])
	uploaded = int(dataarray[1])
	red = int(dataarray[6])
	orange = int(dataarray[5])
	amber = int(dataarray[4])
	yellow = int(dataarray[3])
	green = int(dataarray[2])
	vpnstatus = 0
	temp = -999999.9
	if len(dataarray) > 7:
		if dataarray[7] == "1":
			vpnstatus = 1
		if len(dataarray) > 8:
			temp = float(dataarray[8])


	return HistoryItemClass.DefineItem(datetime, uploaded, red, orange, amber, yellow, green, vpnstatus, temp)


def createblank(datetime):

	return HistoryItemClass.DefineItem(datetime, 0, 0, 0, 0, 0, 0, 1, -999999.9)
