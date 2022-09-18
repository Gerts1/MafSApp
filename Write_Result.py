import os
import csv
from numpy import sqrt, log

def InitWrite(modelType,config,Par):
	ruta = (Par[2][:Par[2].rfind("*")])+'Resultados'
	if os.path.isdir(ruta)==False:
		os.mkdir(ruta)

# Archivo de datos de ajustes
	fpath = os.path.join(ruta, 'Data_Fit.csv')
	Data_Fit=open(fpath,'w',newline='')
	writer=csv.writer(Data_Fit,delimiter=',')

# Archivo Reporte
	fpath0 = os.path.join(ruta, 'Reporte.csv')
	Report=open(fpath0,'w',newline='')
	writer=csv.writer(Report,delimiter=',')

	labs=Make_Labels(config,modelType)

	Data_Fit.write('Archivo,')
	for l in labs:
		Data_Fit.write(l+','+'+-,')	
	Data_Fit.write('\n')

	Hs=config.HS
	Iso_Type=config.Name

	Par19=str(Par[19])
	Par20=str(Par[20])
	Par21=str(Par[21])
	ColX=Par[26][Par[10][0]]
	ColY=Par[26][Par[10][1]]


	Report.write('Reporte del Análisis:\n')
	Report.write(f'Isótopo:,{Iso_Type}\n')
	Report.write(f'Col X:,{ColX}\n')
	Report.write(f'Col Y:,{ColY}\n')
	Report.write(f'TMax:,{Par[5][0]:3.7f},s\n')
	Report.write(f'TMin:,{Par[5][1]:3.7f},s\n')
	Report.write(f'Inversión eje X:,{Par19}\n')
	Report.write(f'Inversión eje Y:,{Par20}\n')

	if Par[27]==False:
		Par6=[]
		for i in range(len(Hs)):
			Par6.append(str(Par[6][i]))

		Report.write(f'Tiempo Dips:\n')
		for i in range(len(Hs)):
			Report.write(f'{Hs[i]}:,{Par6[i]}\n')

		Report.write(f'w Calibración:,{Par[7]:3.7f}\n')
		Report.write(f'Fmax:,{Par[24]:3.7f},MHz\n')
		Report.write(f'Fmin:,{Par[25]:3.7f},MHz\n')
		Report.write(f'Método Calibración:,{Par[11]:3.7f}\n')

	Report.write(f'Temperatura:,{Par[8]:3.7f},K\n')
	Report.write(f'Gauss FWHM:,{Par[9]:3.7f},MHz\n')
	Report.write(f'LWmin:,{Par[12]:3.7f},MHz\n')
	Report.write(f'LWmax:,{Par[13]:3.7f},MHz\n')
	Report.write(f'GSmim:,{Par[14]:3.7f},MHz\n')
	Report.write(f'GSmax:,{Par[15]:3.7f},MHz\n')
	Report.write(f'Dc:,{Par[16]:3.7f},MHz\n')
	Report.write(f'Mismo ancho Lorentziano:,{Par21}\n')
	Report.write(f'\n')
	Report.write(f'Archivos análizados:\n')

	return [Data_Fit,Report]

def WriteDataFit(f,popt,perr,Data_Fit,Trans,modelType,Par1):
	po,pe=Centros(popt,perr,Trans,Par1)
	po,pe=Widths(po,pe,Trans,modelType,Par1)
	Data_Fit.write(f+',')
	for i in range(len(po)):
		Data_Fit.write(str(f'{po[i]:3.7f},'))
		Data_Fit.write(str(f'{pe[i]:3.7f},'))
	Data_Fit.write('\n')

def WriteReport(f,flag,error,Report):
	if flag==True:
		mensaje='Ok'
	else:
		mensaje='Error'

	Report.write(f+','+mensaje+','+error+'\n')

def WriteEspectro(f,frec,Data,SubDoppler,Fit,ruta):
# Archivo de espectro calibrado con su ajuste
	fpath0 = os.path.join(ruta, 'Fit_'+f)
	Espectros=open(fpath0,'w',newline='')
	writer=csv.writer(Espectros,delimiter=',')
	Espectros.write('frec,Data,SubDoppler,Fit\n')
	for i in range(len(frec)):
		Espectros.write(str(f'{frec[i]:3.7f},'))
		Espectros.write(str(f'{Data[i]:3.10f},'))
		Espectros.write(str(f'{SubDoppler[i]:3.10f},'))
		Espectros.write(str(f'{Fit[i]:3.10f}'))
		Espectros.write('\n')
	Espectros.close()


def Make_Labels(config,modelType):
	labs=[]
	leter=['A','C']
	Hs=config.HS
	Iso_Type=config.Name

	if ((modelType == 'Lorentz') or (modelType == 'Voigt') or (modelType == 'Voigt_1L')):
		leter.append('LFWHM')
	elif modelType == 'Gauss':
		leter.append('GFWHM')

	for L in leter:
	    for H in Hs :
	        labs.append(f'{L}'+'_'+f'{H}')
	
	if modelType=='Voigt_1L':
		for i in range(len(Hs)):
			labs.pop(-1)
		labs.append('LFWHM')


	if ((modelType == 'Lorentz') or (modelType == 'Gauss')):
		labs.append('a')
	else:
		labs.append('GFWHM')
		labs.append('a')

	return labs

def Centros(popt,perr,Trans,Par1):
	po=popt
	pe=perr
	if Par1==4:
		j=3
	else:
	    j=6
	for i in range(len(Trans)):
	    po[j+i]=Trans[i]-po[j+i]
	    pe[j+i]=0.5+pe[j+i] #EStoy diciendo que la incertidumbre
        						#de Trans[i] es de +-0.5MHz. Me falta calcularla
	return [po,pe]

def Widths(popt,perr,Trans,modelType,Par1):
	po=popt
	pe=perr
	if Par1==4:
	    s=6
	else:
	    s=12
	c=2*sqrt(2*log(2))

	if modelType=='Gauss':
		for i in range(len(Trans)):
			po[s+i]*=c
			pe[s+i]*=c
	elif modelType=='Lorentz':
		for i in range(len(Trans)):
			po[s+i]*=2
			pe[s+i]*=2
	elif modelType=='Voigt':
		for i in range(len(Trans)):
			po[s+i]*=2
			pe[s+i]*=2
		po[-2]*=c
		pe[-2]*=c
	elif modelType=='Voigt_1L':
		po[-3]*=2
		pe[-3]*=2
		po[-2]*=c
		pe[-2]*=c

	return [po,pe]