from numpy import sqrt, diag, append, real, pi
from scipy.optimize import curve_fit
from scipy.special import wofz
from Config1 import Transicion


class VoigtFit():
	def __init__(self,Par=None,frec=None,SubDoppler=None):
		self.Wmin=Par[12]
		self.Wmax=Par[13]
		self.Gmin=Par[14]
		self.Gmax=Par[15]
		self.dC=Par[16]
		self.frec=frec
		self.SubDoppler=SubDoppler
		self.config=Transicion(Par)
		self.Trans=self.config.Trans

	def Voigt_norm(self,x,sig,w,xc): #Voigth normalizada
		z = ((x-xc)+1j*w)/sig/sqrt(2)
		return real(wofz(z))/sig/sqrt(2*pi)

	def Voigt(self,x,sig,w,xc,h): #Voigth altura h no normalizada
		norm = self.Voigt_norm(xc,sig,w,xc)
		return h*self.Voigt_norm(x,sig,w,xc)/norm

	def Voigt6(self,x,A1,A2,A3,A4,A5,A6,dc1,dc2,dc3,dc4,dc5,dc6,w1,w2,w3,w4,w5,w6,sig,c):#Función Voigt 6 PEAKS
		return  self.Voigt(x,sig,w1,self.Trans[0]-dc1,A1) +\
				self.Voigt(x,sig,w2,self.Trans[1]-dc2,A2) +\
				self.Voigt(x,sig,w3,self.Trans[2]-dc3,A3) +\
				self.Voigt(x,sig,w4,self.Trans[3]-dc4,A4) +\
				self.Voigt(x,sig,w5,self.Trans[4]-dc5,A5) +\
				self.Voigt(x,sig,w6,self.Trans[5]-dc6,A6) + c


	def Voigt3(self,x,A1,A2,A3,dc1,dc2,dc3,w1,w2,w3,sig,c):	#Función Lorentziana 3 PEAKS
		return  self.Voigt(x,sig,w1,self.Trans[0]-dc1,A1) +\
				self.Voigt(x,sig,w2,self.Trans[1]-dc2,A2) +\
				self.Voigt(x,sig,w3,self.Trans[2]-dc3,A3) + c

	def Voigt61L(self,x,A1,A2,A3,A4,A5,A6,dc1,dc2,dc3,dc4,dc5,dc6,w,sig,c):#Función Voigt 6 PEAKS mismo ancho lorentziano
		return  self.Voigt(x,sig,w,self.Trans[0]-dc1,A1) +\
				self.Voigt(x,sig,w,self.Trans[1]-dc2,A2) +\
				self.Voigt(x,sig,w,self.Trans[2]-dc3,A3) +\
				self.Voigt(x,sig,w,self.Trans[3]-dc4,A4) +\
				self.Voigt(x,sig,w,self.Trans[4]-dc5,A5) +\
				self.Voigt(x,sig,w,self.Trans[5]-dc6,A6) + c


	def Voigt31L(self,x,A1,A2,A3,dc1,dc2,dc3,w,sig,c):	#Función Lorentziana 3 PEAKS, mismo ancho lorentziano
		return  self.Voigt(x,sig,w,self.Trans[0]-dc1,A1) +\
				self.Voigt(x,sig,w,self.Trans[1]-dc2,A2) +\
				self.Voigt(x,sig,w,self.Trans[2]-dc3,A3) + c


	def V_Fit6(self):
		A=max(self.SubDoppler)-min(self.SubDoppler)
		wmax=self.Wmax
		wmin=self.Wmin
		Gmin=self.Gmin
		Gmax=self.Gmax
		dc=self.dC
		c=0
		PIn=[A,A,A,A,A,A,0,0,0,0,0,0,wmax,wmax,wmax,wmax,wmax,wmax,Gmax,c]
		p_b=([0,-A,0,0,0,0,-dc,-dc,-dc,-dc,-dc,-dc,wmin,wmin,wmin,wmin,wmin,wmin,Gmin,-10],\
			[A,A,A,A,A,A,dc,dc,dc,dc,dc,dc,wmax,wmax,wmax,wmax,wmax,wmax,Gmax,10])

		popt,pcov = curve_fit(self.Voigt6,self.frec,self.SubDoppler,p0=PIn,bounds=p_b,absolute_sigma=False)
		perr=sqrt(diag(pcov))
		return [popt,perr]

	def V_Fit3(self):
		A=max(self.SubDoppler)-min(self.SubDoppler)
		wmax=self.Wmax
		wmin=self.Wmin
		Gmin=self.Gmin
		Gmax=self.Gmax
		dc=self.dC
		c=0
		PIn=[A,A,A,0,0,0,wmax,wmax,wmax,Gmax,c]
		p_b=([0,0,0,-dc,-dc,-dc,wmin,wmin,wmin,Gmin,-10],\
			[A,A,A,dc,dc,dc,wmax,wmax,wmax,Gmax,10])

		popt,pcov = curve_fit(self.Voigt3,self.frec,self.SubDoppler,p0=PIn,bounds=p_b,absolute_sigma=False)
		perr=sqrt(diag(pcov))
		return [popt,perr]

	def V_Fit61L(self):
		A=max(self.SubDoppler)-min(self.SubDoppler)
		wmax=self.Wmax
		wmin=self.Wmin
		Gmin=self.Gmin
		Gmax=self.Gmax
		dc=self.dC
		c=0
		PIn=[A,A,A,A,A,A,0,0,0,0,0,0,wmax,Gmax,c]
		p_b=([0,-A,0,0,0,0,-dc,-dc,-dc,-dc,-dc,-dc,wmin,Gmin,-10],\
			[A,A,A,A,A,A,dc,dc,dc,dc,dc,dc,wmax,Gmax,10])

		popt,pcov = curve_fit(self.Voigt61L,self.frec,self.SubDoppler,p0=PIn,bounds=p_b,absolute_sigma=False)
		perr=sqrt(diag(pcov))
		return [popt,perr]

	def V_Fit31L(self):
		A=max(self.SubDoppler)-min(self.SubDoppler)
		wmax=self.Wmax
		wmin=self.Wmin
		Gmin=self.Gmin
		Gmax=self.Gmax
		dc=self.dC
		c=0
		PIn=[A,A,A,0,0,0,wmax,Gmax,c]
		p_b=([0,0,0,-dc,-dc,-dc,wmin,Gmin,-10],\
			[A,A,A,dc,dc,dc,wmax,Gmax,10])

		popt,pcov = curve_fit(self.Voigt31L,self.frec,self.SubDoppler,p0=PIn,bounds=p_b,absolute_sigma=False)
		perr=sqrt(diag(pcov))
		return [popt,perr]