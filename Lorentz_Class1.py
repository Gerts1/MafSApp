from numpy import sqrt, diag, append
from scipy.optimize import curve_fit
from Config1 import Transicion

class LorentzFit():
	def __init__(self,Par=None,frec=None,SubDoppler=None):
		self.Wmin=Par[12]
		self.Wmax=Par[13]
		self.dC=Par[16]
		self.frec=frec
		self.SubDoppler=SubDoppler
		self.config=Transicion(Par)
		self.Trans=self.config.Trans

	def lorentz6(self,x,A1,A2,A3,A4,A5,A6,dc1,dc2,dc3,dc4,dc5,dc6,w1,w2,w3,w4,w5,w6,c):#Función Lorentziana 6 PEAKS
		return (A1*w1**2/((x-self.Trans[0]+dc1)**2+w1**2)) +\
    			(A2*w2**2/((x-self.Trans[1]+dc2)**2+w2**2)) +\
    			(A3*w3**2/((x-self.Trans[2]+dc3)**2+w3**2)) +\
    			(A4*w4**2/((x-self.Trans[3]+dc4)**2+w4**2)) +\
    			(A5*w5**2/((x-self.Trans[4]+dc5)**2+w5**2)) +\
    			(A6*w6**2/((x-self.Trans[5]+dc6)**2+w6**2)) + c

	def lorentz3(self,x,A1,A2,A3,dc1,dc2,dc3,w1,w2,w3,c):	#Función Lorentziana 3 PEAKS
		return (A1*w1**2/((x-self.Trans[0]+dc1)**2+w1**2)) +\
    			(A2*w2**2/((x-self.Trans[1]+dc2)**2+w2**2)) +\
    			(A3*w3**2/((x-self.Trans[2]+dc3)**2+w3**2)) + c


	def L_Fit6(self):
		A=max(self.SubDoppler)-min(self.SubDoppler)
		wmax=self.Wmax
		wmin=self.Wmin
		dc=self.dC
		c=0
		PIn=[A,A,A,A,A,A,0,0,0,0,0,0,wmax,wmax,wmax,wmax,wmax,wmax,c]
		#p_b=([0,-A,0,0,0,0,-dc,-dc,-dc,-dc,-dc,-dc,wmin,wmin,wmin,wmin,wmin,wmin,-10],\
		p_b=([-A,-A,-A,-A,-A,-A,-dc,-dc,-dc,-dc,-dc,-dc,wmin,wmin,wmin,wmin,wmin,wmin,-10],\
			[A,A,A,A,A,A,dc,dc,dc,dc,dc,dc,wmax,wmax,wmax,wmax,wmax,wmax,10])
		#p_b=([0,0,0,0,0,0,-dc,-dc,-dc,-dc,-dc,-dc,wmin,wmin,wmin,wmin,wmin,wmin],\
		#	[A,A,A,A,A,A,dc,dc,dc,dc,dc,dc,wmax,wmax,wmax,wmax,wmax,wmax])

		self.popt,pcov = curve_fit(self.lorentz6,self.frec,self.SubDoppler,p0=PIn,bounds=p_b)
		self.perr=sqrt(diag(pcov))
		return [self.popt,self.perr]

	def L_Fit3(self):
		A=max(self.SubDoppler)-min(self.SubDoppler)
		wmax=self.Wmax
		wmin=self.Wmin
		dc=self.dC
		c=0
		PIn=[A,A,A,0,0,0,wmax,wmax,wmax,0]
		p_b=([0,0,0,-dc,-dc,-dc,wmin,wmin,wmin,-10],\
			[A,A,A,dc,dc,dc,wmax,wmax,wmax,10])

		popt,pcov = curve_fit(self.lorentz3,self.frec,self.SubDoppler,p0=PIn,bounds=p_b)
		perr=sqrt(diag(pcov))

		return [popt,perr]