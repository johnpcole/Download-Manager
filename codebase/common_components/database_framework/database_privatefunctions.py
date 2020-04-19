def buildfieldssql(rawdata, concatenator, parameterise):

	fieldlist = ""

	for fieldname in sorted(rawdata.keys()):
		if fieldname != 'recordtype':
			if fieldlist != "":
				fieldlist = fieldlist + concatenator
			fieldlist = fieldlist + fieldname
			if parameterise is True:
				fieldlist = fieldlist + " = ?"

	return fieldlist



def buildvaluessql(rawdata):

	valuelist = []

	for fieldname in sorted(rawdata.keys()):
		if fieldname != 'recordtype':
			valuelist.append(rawdata[fieldname])

	return valuelist



def buildparameterssql(rawdata):

	parameterlist = ""

	for fieldname in rawdata.keys():
		if fieldname != 'recordtype':
			if parameterlist != "":
				parameterlist = parameterlist + ", "
			parameterlist = parameterlist + "?"
	parameterlist = " VALUES (" + parameterlist + ")"

	return parameterlist



def buildresult(rawdata, selectoutcome):

	outcome = {}

	indexer = -1
	for fieldname in sorted(rawdata.keys()):
		if fieldname != 'recordtype':
			indexer = indexer + 1
			outcome[fieldname] = selectoutcome[indexer]

	return outcome