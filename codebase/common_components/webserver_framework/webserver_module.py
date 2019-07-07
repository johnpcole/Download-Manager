import flask as FlaskApplication




def createwebsite(websitename):
	return FlaskApplication.Flask(websitename, template_folder='webassets/templates', static_folder='webassets')



def getrequestdata():
	return FlaskApplication.request.get_json()



def makehtml(*args, **kwargs):
	return FlaskApplication.render_template(*args, **kwargs)



def makejson(**kwargs):
	return FlaskApplication.jsonify(**kwargs)



