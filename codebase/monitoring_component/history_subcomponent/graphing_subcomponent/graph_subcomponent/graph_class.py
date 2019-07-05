
class DefineGraph:

	def __init__(self):

		self.dictionary = {"brightred": [], "red": [], "orange": [], "amber": [], "yellow": [], "green": [], "blue": [],
												"tempa": [], "tempb": [], "tempc": [], "tempd": [], "tempe": [],
												"axeslines": [], "biglabels": [], "littlelabels": [], "graphtitles": []}



	def mergein(self, othergraphtomergein):

		for key in self.dictionary.keys():
			mergedlist = []
			mergedlist.extend(self.dictionary[key])
			mergedlist.extend(othergraphtomergein.dictionary[key])
			self.dictionary[key] = mergedlist



	def get(self):

		return self.dictionary


	def additem(self, elementtype, instructionobject):

		self.dictionary[elementtype].append(instructionobject)

