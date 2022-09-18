class name():
	def __init__(self,nam=None):
		self.nam=nam
		self.say_may_name()

	def say_may_name(self):
		a=self.nam.find('\\')+1
		b=len(self.nam)
		self.nam=self.nam[a:b]