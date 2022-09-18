from numpy import zeros, delete
from pandas import read_csv 
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from Config1 import Transicion
from Invertir import Inv_Eje_Y,Inv_Eje_X

class Calibracion():
    def __init__(self,Par=None,file=None):
        self.Par=Par
        self.file = file
        self.xmax=Par[5][0]
        self.xmin=Par[5][1]
        self.tims=Par[6]
        self.W=Par[7]
        self.dist=[]
        self.T=[]
        self.frec=None
        self.Volt=None
        if self.Par[27]==0:
            self.config=Transicion(self.Par)
            self.Data_dist()
            self.Dist_Ref()
        else:
            self.NoCal()


    
    def Data_dist(self):
        for i in range(len(self.config.HS)):
            self.dist.append(0)
            self.T.append(0)

    def Dist_Ref(self):
        ind=self.config.Ref[1]
        for i in range(len(self.config.HS)):
            self.dist[i]=self.tims[ind]-self.tims[i]

    def Cal1(self):
        xmax=self.xmax
        xmin=self.xmin
        w=self.W
        datos = read_csv(self.file,header=self.Par[3])
        self.x = datos.values[:,self.Par[10][0]]
        self.y = datos.values[:,self.Par[10][1]]
        if self.Par[20]==True:
            self.y=Inv_Eje_Y(self.y)
        if self.Par[19]==True:
            self.x=Inv_Eje_X(self.x)
        mask = ((self.tims[3]+self.tims[4])/2<= self.x)*(self.x <= self.tims[5]+(self.dist[5]/2)) 
        Time = self.x[mask]
        Volt = self.y[mask]
        #print('xmin, xmax:',Time[0],Time[-1])

        mul=-1
        if self.Par[1]==4:
            mul=1

        alto=max(Volt*mul)
        #print('alto=',alto*-1)
        ref,_=find_peaks(Volt*mul,height=alto,width=w)
        #print('pico=',ref)

        for i in range(len(self.config.HS)):
            self.T[i]=Time[ref][0]-self.dist[i]
        popt,_ = curve_fit(self.linear,self.T,self.config.Trans)  
        self.x = datos.values[:,self.Par[10][0]]
        self.y = datos.values[:,self.Par[10][1]]
        if self.Par[20]==True:
            self.y=Inv_Eje_Y(self.y)
        if self.Par[19]==True:
            self.x=Inv_Eje_X(self.x)
        mask = (xmin <= self.x)*(self.x <= xmax) 
        Time = self.x[mask]
        Volt = self.y[mask]
        self.frec=zeros(len(Time))
        self.frec=popt[1]*Time+popt[0]
        self.Volt=Volt



    def NoCal(self):
        xmax=self.xmax
        xmin=self.xmin
        datos = read_csv(self.file,header=self.Par[3])
        self.x = datos.values[:,self.Par[10][0]]
        self.y = datos.values[:,self.Par[10][1]]
        if self.Par[20]==True:
            self.y=Inv_Eje_Y(self.y)
        if self.Par[19]==True:
            self.x=Inv_Eje_X(self.x)

        mask = (xmin <= self.x)*(self.x <= xmax) 
        self.frec = self.x[mask]
        self.Volt = self.y[mask]




    def linear(self,x,A,B):          #Función Lineal
        return B*x+A


    def Cal(self):
        xmax=self.xmax
        xmin=self.xmin
        w=self.W
        datos = read_csv(self.file,header=self.Par[3])
        self.x = datos.values[:,self.Par[10][0]]
        self.y = datos.values[:,self.Par[10][1]]
        if self.Par[20]==True:
            self.y=Inv_Eje_Y(self.y)
        if self.Par[19]==True:
            self.x=Inv_Eje_X(self.x)
        mask = (xmin <= self.x)*(self.x <= xmax) 
        Time = self.x[mask]
        Volt = self.y[mask]
        self.frec=zeros(len(Time))

        mul=-1
        if self.Par[1]==4:
            mul=1

        alto=max(Volt*mul)
        ref,_=find_peaks(Volt*mul,height=alto,width=w)
        #print('picos:',ref)
        for i in range(len(self.config.HS)):
            self.T[i]=Time[ref][0]-self.dist[i]
        popt,_ = curve_fit(self.linear,self.T,self.config.Trans)     
        self.frec=popt[1]*Time+popt[0]
        self.Volt=Volt


    def Cal2(self):
        xmax=self.xmax
        xmin=self.xmin
        w=self.W
        datos = read_csv(self.file,header=self.Par[3])
        self.x = datos.values[:,self.Par[10][0]]
        self.y = datos.values[:,self.Par[10][1]]
        if self.Par[20]==True:
            self.y=Inv_Eje_Y(self.y)
        if self.Par[19]==True:
            self.x=Inv_Eje_X(self.x)
        mask = (xmin <= self.x)*(self.x <= xmax) 
        Time = self.x[mask]
        Volt = self.y[mask]
        self.frec=zeros(len(Time))

        mul=-1
        if self.Par[1]==4:
            mul=1

        alto=max(Volt*mul)
        bajo=min(Volt*mul)
        d=alto-bajo
        L=alto-0.10*d
        ref0,_=find_peaks(Volt*mul,height=L,width=w)
        print(Time[ref0])

        #print('picos:',ref)
        for i in range(len(self.config.HS)):
            self.T[i]=Time[ref0][0]-self.dist[i]
        popt,_ = curve_fit(self.linear,self.T,self.config.Trans)     
        self.frec=popt[1]*Time+popt[0]
        self.Volt=Volt