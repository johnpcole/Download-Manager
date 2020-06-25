from . import copier_class as CopierClass

def createcopier(copieractionqueuelocation, copierresultslocation, copierappconfiglocation):

	return CopierClass.DefineCopier(copieractionqueuelocation, copierresultslocation, copierappconfiglocation)

