from . import historyitem_class as HistoryItemClass


def createhistoryitem(datetime, uploadeddelta, redcount, ambercount, greencount):
	return HistoryItemClass.DefineItem(datetime, uploadeddelta, redcount, ambercount, greencount)

