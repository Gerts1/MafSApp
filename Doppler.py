from numpy import sqrt, log

class DopplerW():
	def __init__(self,Par=None):
		self.Par=Par
		self.T=Par[8]
		self.w=0
		self.m=0
		self.Lamb=1
		self.masa()
		self.Long_Ond()
		self.W_Doppler()

	def W_Doppler(self):
		Kb=1.38065e-23
		c=299792458
		kg=self.m*1.6605402e-27
		Vp=sqrt(2*Kb*self.T/kg)
		l=c*1000/self.Lamb
		self.FWHM=2*sqrt(log(2))*l*Vp/c
		self.sig=l*Vp/(sqrt(2)*c)

	def Long_Ond(self):
		if (self.Par[1]==0 or self.Par[1]==1):
			self.Lamb=780
		elif (self.Par[1]==2 or self.Par[1]==3):
			self.Lamb=420
    
	def masa(self):
		if self.Par[0]=='A':
			self.m=86.909180520
		elif self.Par[0]=='B':
			self.m=84.911789732