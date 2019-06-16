import flask as FlaskApplication



#from flask import render_template as Webpage
#from flask import jsonify as Jsondata



def createwebsite():
	return FlaskApplication.Flask(__name__, template_folder='../../../webassets/templates', static_folder='../../../webassets')



def getrequestdata():
	return FlaskApplication.request.get_json()



def makehtml(templatename, **kwargs):
	return FlaskApplication.render_template(templatename, kwargs)

