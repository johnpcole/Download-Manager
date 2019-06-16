import flask as FlaskApplication



#from flask import render_template as Webpage
#from flask import jsonify as Jsondata
#from flask import request as Webpost



def createwebsite():
	return FlaskApplication.Flask(__name__, template_folder='../../../webassets/templates')





