from numpy import zeros, exp, append, sqrt, log
from scipy.optimize import curve_fit
from Config1 import Transicion

class FGauss():
	def __init__(self,Par=None,frec=None,Volt=None):
		self.Par=Par
		self.sig=Par[9]/(2*sqrt(2*log(2)))
		self.config=Transicion(self.Par)
		self.Trans=self.config.Trans
		self.CutPorcentaje= abs((self.Trans[0]-self.Trans[0]))*0.1
		self.FondoGaussiano(frec,Volt)
		#self.FondoGaussiano2(frec,Volt)


	def gaus3(self,x,A1,A2,A3,c):	#Función Gaussiana 3 PEAKS
		return A1*exp(-0.5*((x-self.Trans[0])/self.sig)**2)+\
				A2*exp(-0.5*((x-self.Trans[2])/self.sig)**2)+\
				A3*exp(-0.5*((x-self.Trans[5])/self.sig)**2) + c

	def gaus32(self,x,m,AG1,AG2,AG3,c):	#Función Gaussiana 3 PEAKS
		return m*x +\
				AG1*exp(-0.5*((x-self.Trans[0])/self.sig)**2)+\
				AG2*exp(-0.5*((x-self.Trans[2])/self.sig)**2)+\
				AG3*exp(-0.5*((x-self.Trans[5])/self.sig)**2) + c

	def gaus33(self,x,A1,A2,A3,x1,x2,x3,c):	#Función Gaussiana 3 PEAKS
		return A1*exp(-0.5*((x-x1)/self.sig)**2)+\
				A2*exp(-0.5*((x-x2)/self.sig)**2)+\
				A3*exp(-0.5*((x-x3)/self.sig)**2) + c

	def FondoGaussiano(self,frec,Volt):
		mask1 = ((self.Trans[0]-5) > frec)
		mask2 = ((self.Trans[5]+20) < frec)
		#mask1 = ((self.Trans[0]-self.CutPorcentaje) > frec)
		#mask2 = ((self.Trans[5]+self.CutPorcentaje) < frec)
		#mask1 = ((self.Trans[0]) > frec)
		#mask2 = ((self.Trans[5]) < frec)
		T1 = frec[mask1] 
		V1 = Volt[mask1]
		T1=append(T1,frec[mask2])
		V1=append(V1,Volt[mask2])		

		A1=max(V1)
		A2=max(V1)
		A3=max(V1)
		c=0
		p_b=([0,0,0,-A1],[A1,A1,A1,A1])

		popt,_ = curve_fit(self.gaus3,T1,V1,p0=[A1,A2,A3,c])#,bounds=p_b)
		#print(popt)
		
		self.GausFit3=self.gaus3(frec,*popt)
		self.SubDoppler=self.GausFit3-Volt

	def FondoGaussiano2(self,frec,Volt):
		#mask1 = ((self.Trans[0]-5) > frec)
		#mask2 = ((self.Trans[5]+10) < frec)
		mask1 = ((self.Trans[0]-self.CutPorcentaje) > frec)
		mask2 = ((self.Trans[5]+self.CutPorcentaje) < frec)
		#mask1 = ((self.Trans[0]) > frec)
		#mask2 = ((self.Trans[5]) < frec)
		T1 = frec[mask1] 
		V1 = Volt[mask1]
		T1=append(T1,frec[mask2])
		V1=append(V1,Volt[mask2])		

		AG1=max(V1)
		AG2=max(V1)
		AG3=max(V1)
		m = 0
		c = 0
		Pi=[m,AG1,AG2,AG3,c]
		p_b=([-10,0,0,0,-10],[10,AG1,AG1,AG3,10])

		popt,_ = curve_fit(self.gaus32,frec,Volt,p0=Pi,bounds=p_b)
		print(popt)		
		self.GausFit3=self.gaus32(frec,*popt)
		self.SubDoppler=self.GausFit3-Volt

