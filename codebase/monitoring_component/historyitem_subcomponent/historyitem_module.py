from . import historyitem_class as HistoryItemClass


def createhistoryitem(datetime, sessiondata):
	return HistoryItemClass.DefineItem(datetime, sessiondata)

