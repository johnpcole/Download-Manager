from . import pointermeter_class as PointerMeterClass
from . import blockmeter_class as BlockMeterClass


def createlinearmeter(minvalue, maxvalue, needletype):
	return PointerMeterClass.DefinePointerMeter(minvalue, maxvalue, needletype)


def createlogarithmicmeter(maxorderofmagnitude, needletype):
	return PointerMeterClass.DefinePointerMeter(-9999.9, maxorderofmagnitude, needletype)


def createblockmeter(metertype):
	return BlockMeterClass.DefineBlockMeter(metertype)

