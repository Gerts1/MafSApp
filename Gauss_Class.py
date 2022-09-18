from numpy import sqrt, diag, append, exp
from scipy.optimize import curve_fit
from Config1 import Transicion

class GaussFit():
	def __init__(self,Par=None,frec=None,SubDoppler=None):
		self.Gmin=Par[14]
		self.Gmax=Par[15]
		self.dC=Par[16]
		self.frec=frec
		self.SubDoppler=SubDoppler
		self.config=Transicion(Par)
		self.Trans=self.config.Trans

	def gauss3(self,x,A1,A2,A3,dc1,dc2,dc3,sig1,sig2,sig3,c):	#Función Gaussiana 3 PEAKS
		return A1*exp(-0.5*((x-self.Trans[0]+dc1)/sig1)**2)+\
				A2*exp(-0.5*((x-self.Trans[1]+dc2)/sig2)**2)+\
				A3*exp(-0.5*((x-self.Trans[2]+dc3)/sig3)**2) + c

	def gauss6(self,x,A1,A2,A3,A4,A5,A6,dc1,dc2,dc3,dc4,dc5,dc6,sig1,sig2,sig3,sig4,sig5,sig6,c):	#Función Gaussiana 6 PEAKS
		return A1*exp(-0.5*((x-self.Trans[0]+dc1)/sig1)**2)+\
				A2*exp(-0.5*((x-self.Trans[1]+dc2)/sig2)**2)+\
				A3*exp(-0.5*((x-self.Trans[2]+dc3)/sig3)**2)+\
				A4*exp(-0.5*((x-self.Trans[3]+dc4)/sig4)**2)+\
				A5*exp(-0.5*((x-self.Trans[4]+dc5)/sig5)**2)+\
				A6*exp(-0.5*((x-self.Trans[5]+dc6)/sig6)**2) + c


	def G_Fit6(self):
		A=max(self.SubDoppler)-min(self.SubDoppler)
		wmax=self.Gmax
		wmin=self.Gmin
		dc=self.dC
		c=0
		PIn=[A,A,A,A,A,A,0,0,0,0,0,0,wmax,wmax,wmax,wmax,wmax,wmax,c]
		p_b=([0,-A,0,0,0,0,-dc,-dc,-dc,-dc,-dc,-dc,wmin,wmin,wmin,wmin,wmin,wmin,-10],\
			[A,A,A,A,A,A,dc,dc,dc,dc,dc,dc,wmax,wmax,wmax,wmax,wmax,wmax,10])


		self.popt,pcov = curve_fit(self.gauss6,self.frec,self.SubDoppler,p0=PIn,bounds=p_b)
		self.perr=sqrt(diag(pcov))
		return [self.popt,self.perr]

	def G_Fit3(self):
		A=max(self.SubDoppler)-min(self.SubDoppler)
		wmax=self.Gmax
		wmin=self.Gmin
		dc=self.dC
		c=0
		PIn=[A,A,A,0,0,0,wmax,wmax,wmax,0]
		p_b=([0,0,0,-dc,-dc,-dc,wmin,wmin,wmin,-10],\
			[A,A,A,dc,dc,dc,wmax,wmax,wmax,10])

		self.popt,pcov = curve_fit(self.gauss3,self.frec,self.SubDoppler,p0=PIn,bounds=p_b)
		self.perr=sqrt(diag(pcov))
		return [self.popt,self.perr]