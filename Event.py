class Event(object):

	def __init__(self): self.callback = None
	def __call__(self, *args, **keywargs): self.callback(*args, **keywargs)

	# sets the callback for this event
	def set(self, func): self.callback = func
