def rectangle(x, y, w, h):

	outcome = {}
	outcome["x"] = x
	outcome["y"] = y
	outcome["w"] = w
	outcome["h"] = h
	return outcome



def line(x, y, w, h):

	outcome = {}
	outcome["xa"] = x
	outcome["ya"] = y
	outcome["xb"] = w + x
	outcome["yb"] = h + y
	return outcome



def text(x, y, t):

	outcome = {}
	outcome["x"] = x
	outcome["y"] = y
	outcome["t"] = t
	return outcome