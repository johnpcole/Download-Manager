def getcopieractiondescription(copyid, copieritem):

	data = copieritem.getcopieractioninstruction(copyid)

	if data['action'] == "Scrape TV Shows":
		outcome = "Request " + copyid + " sent to copier to scrape TV Show folders"

	elif data['action'] == "Copy File":
		space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
		arrows = space + space + "&darr;"
		indent = space + space + space + space + space
		lineofarrows = arrows + arrows + arrows + arrows + arrows
		outcome = "Request " + copyid + " sent to copier to Copy File:</br>" + indent + data['source'] + "</br>"
		outcome = outcome + indent + lineofarrows + "</br>" + indent + data['target']

	else:
		outcome = "Unknown Action Type"

	return outcome

