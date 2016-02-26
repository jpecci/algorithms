class BaseEvent:
	pass

class Zero(BaseEvent):
	pass

class AnyEvent(BaseEvent):
	pass

def combine(e1, e2):
	return AnyEvent()

es=(AnyEvent() for i in range(10))

reduce(combine, es)