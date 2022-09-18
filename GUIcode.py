import matplotlib
matplotlib.use('TkAgg')
from tkinter import Tk,Frame,IntVar,\
    Label,Button,Entry,filedialog,messagebox,END,Radiobutton,PhotoImage,Checkbutton
from tkinter.ttk import Combobox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import SpanSelector

from glob import glob
from pandas import read_csv 
from numpy import delete
from fastnumbers import isfloat
from math import isnan
from matplotlib.pyplot import plot, close

from tkinter.font import Font
from Name import name

from Invertir import Inv_Eje_Y,Inv_Eje_X


################################################
#Selecciona el isotopo:
class Win1(Frame):
    def __init__(self, master=None,Par=None):
        super().__init__(master,width=400,height=200,bg="#49A")
        self.isotopo = IntVar()
        self.Par=Par
        self.fontT=self.master.fontT
        self.fontl=self.master.fontl
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        Label(self,text='Selecciona el isótopo:',
                    bg="#49A",font=self.fontT).grid(row=0,column=1)
        self.A=Radiobutton(self,text='Rb 87',bg="#49A",
            variable=self.isotopo,value=1,
            command=self.SelIso,font=self.fontl)
        self.A.select()
        self.A.grid(row=1,column=1)
        Radiobutton(self,text='Rb 85',bg="#49A",
            variable=self.isotopo,value=2,
            command=self.SelIso,font=self.fontl).grid(row=2,column=1)
        Button(self,text='Continuar',width=20,
            command=self.Next1,font=self.fontl).grid(row=5,column=2)
        Button(self,text='Cerrar',width=20,
            command=self.master.destroy,font=self.fontl).grid(row=5,column=0)

    def SelIso(self):
        if self.isotopo.get()==1:
            self.Par[0]='A'
        elif self.isotopo.get()==2:
            self.Par[0]='B'

    def Next1(self):
        self.master.switch_frame(Win2,self.Par)
#######################################################
# Selecciona la transición
class Win2(Frame):
    def __init__(self, master=None,Par=None):
        super().__init__(master,width=400,height=200,bg="#49A")
        self.Transicion = IntVar()
        self.Par=Par
        self.fontT=self.master.fontT
        self.fontl=self.master.fontl
        self.master = master
        self.pack()
        self.opciones=['5S1/2 F=1 -> 5P3/2',
                       '5S1/2 F=2 -> 5P3/2',
                       '5S1/2 F=1 -> 6P3/2',
                       '5S1/2 F=2 -> 6P3/2',
                       '5P3/2 F=3 -> 5D5/2']
        self.OP()
        self.create_widgets()

    def OP(self):
        if self.Par[0]=='A':
            self.opciones=['5S1/2 F=1 -> 5P3/2',
                           '5S1/2 F=2 -> 5P3/2',
                           '5S1/2 F=1 -> 6P3/2',
                           '5S1/2 F=2 -> 6P3/2',
                           '5P3/2 F=3 -> 5D5/2']
        elif self.Par[0]=='B':
            self.opciones=['5S1/2 F=2 -> 5P3/2',
                           '5S1/2 F=3 -> 5P3/2',
                           '5S1/2 F=2 -> 6P3/2',
                           '5S1/2 F=3 -> 6P3/2',
                           '5P3/2 F=3 -> 5D5/2']
        

    def create_widgets(self):
        Label(self,text='Selecciona la transición:',
                    bg="#49A",font=self.fontT).grid(row=0,column=1)
        self.CombOp=Combobox(self,width=20,values=self.opciones,
            state='readonly',font=self.fontl)
        self.CombOp.grid(row=1,column=1)
        self.CombOp.current(0)
        Button(self,text='Continuar',width=20,
            command=self.Next1,font=self.fontl).grid(row=5,column=2)
        Button(self,text='Regresar',width=20,
            command=self.Back1,font=self.fontl).grid(row=5,column=0)

    def SelTran(self):
        if self.CombOp.get()==self.opciones[0]:
            self.Par[1]=0
        elif self.CombOp.get()==self.opciones[1]:
            self.Par[1]=1
        elif self.CombOp.get()==self.opciones[2]:
            self.Par[1]=2
        elif self.CombOp.get()==self.opciones[3]:
            self.Par[1]=3
        elif self.CombOp.get()==self.opciones[4]:
            self.Par[1]=4

    def Next1(self):
        self.SelTran()
        self.master.switch_frame(Win3,self.Par)

    def Back1(self):
        self.Par=['A',0,0,0]
        self.master.switch_frame(Win1,self.Par)

#######################################################
#Selecciona la carpeta
class Win3(Frame):
    def __init__(self, master=None,Par=None):
        super().__init__(master,width=400,height=200,bg="#49A")
        self.Par=Par
        self.fontT=self.master.fontT
        self.fontl=self.master.fontl
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        Label(self,text='Selecciona un Directorio:',
            bg="#49A",font=self.fontT).grid(row=0,column=1)
        Label(self, text=r'Dir:',width=5,font=self.fontl).grid(row=1,column=0)
        self.Dir=Entry(self,width=30,font=self.fontl,state='disable')
        self.Dir.grid(row=1,column=1)
        Button(self,text='Abrir',width=4,
            command=self.AbrirF,font=self.fontl).grid(row=1,column=2)
        Button(self,text='Continuar',width=20,
            command=self.Next1,font=self.fontl).grid(row=5,column=2)
        Button(self,text='Regresar',width=20,
            command=self.Back1,font=self.fontl).grid(row=5,column=0)

    def AbrirF(self):
        self.Par[2]=filedialog.askdirectory(title='Abrir')
        self.Dir['state']='normal'
        self.Dir.delete(0,END)
        self.Dir.insert(END,self.Par[2])
        self.Dir['state']='disable'
        self.Par[2]=self.Par[2]+'/*.csv'

    def Next1(self):
        if self.Par[2]==0:
            return 0
        else:
            if len(glob(self.Par[2]))==0:
                messagebox.showerror("Error", 'Esta carpeta no contiene archivos CSV validos!!')
                return 0
            else:
                self.master.switch_frame(Win4,self.Par)


    def Back1(self):
        self.Par[2]=0
        self.Par[1]=0
        self.master.switch_frame(Win2,self.Par)

#######################################################
#Seleccionar columnas de datos:

class Win4(Frame):
    def __init__(self, master=None,Par=None):
        super().__init__(master,width=400,height=200,bg="#49A")
        self.Par=Par
        self.header=0
        self.fontT=self.master.fontT
        self.fontl=self.master.fontl
        self.xmax=None
        self.xmin=None
        self.step=0
        self.files=None
        self.colX=0
        self.colY=1
        self.master = master
        self.opciones = []
        self.Find_Header()
        self.create_widgets()

    def create_widgets(self):
        Label(self,text='Columnas de Datos:',
            bg="#49A",font=self.fontT).grid(row=0,column=0)
        Label(self, text=r'Col x',width=10,font=self.fontl).grid(row=1,column=1)
        Label(self, text=r'Col y',width=10,font=self.fontl).grid(row=1,column=2)
        self.CombOpX=Combobox(self,width=20,values=self.opciones,
            state='readonly',font=self.fontl)
        self.CombOpX.grid(row=2,column=1)
        self.CombOpX.current(0)   
        self.CombOpY=Combobox(self,width=20,values=self.opciones,
            state='readonly',font=self.fontl)
        self.CombOpY.grid(row=2,column=2)
        self.CombOpY.current(1)              

        Button(self,text='Continuar',width=20,
            command=self.Next1,font=self.fontl).grid(row=5,column=3)
        Button(self,text='Regresar',width=20,
            command=self.Back1,font=self.fontl).grid(row=5,column=0)


    def Find_Header(self):
        files = glob(self.Par[2])
        for i in range(100):
            a=1
            try:
                datos = read_csv(files[0],header=i)
            except:
                a=0
            if a==0:
                continue
            else:
                #print('se abrió en el intento i:',i)
                break
        x = datos.values[:,0]
        y = datos.values[:,1]
        for j in range(100):
            a=1
            try:
                fig = Figure()
                ax1 = fig.add_subplot(111)
                ax1.plot(x,y)
                #close('all')
            except:
                a=0
                datos = read_csv(files[0],header=j+i)
                x = datos.values[:,0]
                y = datos.values[:,1]
            if a==0:
                continue
            else:
                #print('se ploteó en el intento j:',j)
                break
        self.Par[3]=j+i
        #print('header:',self.Par[3])
############################################
        if self.Par[3]==0:
            self.Par[3]=0
            header=None
        elif j+i-1<0:
            self.Par[3]=0
            header=None
        else:
            header=j+i-1

#############################################
        datos = read_csv(files[0],header=header,skip_blank_lines=False)
        for i in datos.values[0,:]:
            self.opciones.append(i)
        self.Par[26]=self.opciones



    def SelCols(self):
        #print(self.opciones)
        for i in range(len(self.opciones)):
            if self.CombOpX.get()==self.opciones[i]:
                self.colX=i
            for i in range(len(self.opciones)):
                if self.CombOpY.get()==self.opciones[i]:
                    self.colY=i


    def Next1(self):
        self.SelCols()
        r=[self.colX,self.colY]
        #print('clox=',self.colX,' colY=',self.colY)
        self.Par[10]=r
        #close('all')
        self.master.switch_frame(WinRango,self.Par)


    def Back1(self):
        self.Par[10]=0
        self.Par[2]=0
        close('all')
        self.master.switch_frame(Win3,self.Par)

#######################################################

class WinRango(Frame):
    
    def __init__(self, master=None,Par=None):
        super().__init__(master,width="1240", height="680",bg="#49A")
        self.Par=Par
        self.fontT=self.master.fontT
        self.fontl=self.master.fontl
        self.fontAxis=self.master.fontAxis
        self.master = master
        self.x = []
        self.y = []
        self.xmax=0
        self.xmin=0
        self.step = 0
        self.ax1 = None
        self.files = Par[4]
        self.flag = True
        self.index = -1
        self.Inv_Y = IntVar()
        self.Inv_X = IntVar()
        self.SkipCal = IntVar()
        self.figR=PhotoImage(file='nextFig.png')
        self.figL=PhotoImage(file='prevFig.png')
        self.pack(side='top')
        self.Op_files()
        self.create_Databox()
        self.create_framegraficos()


    def create_Databox(self):

        Label(self,text='Selecciona el rango de datos:',
            bg="#49A",font=self.fontT).place(x=500,y=10)

        Databox = Frame(self, width="200", height="600")
        Databox.place(x=20,y=45)

        Label(Databox).grid(row=0,column=0)
        Label(Databox,text='Tmax:',font=self.fontl).grid(row=1,column=0)
        self.Tmax=Entry(Databox,width=20,font=self.fontl)
        self.Tmax.grid(row=2,column=0)
        Label(Databox).grid(row=3,column=0)
        Label(Databox,text='Tmin:',font=self.fontl).grid(row=4,column=0)
        self.Tmin=Entry(Databox,width=20,font=self.fontl)
        self.Tmin.grid(row=5,column=0)
        Label(Databox).grid(row=6,column=0)
        self.CheckD=Checkbutton(Databox,text='Invertir eje Y',variable=self.Inv_Y,\
            onvalue=True,offvalue=False,command=self.Inertir_Y,font=self.fontl)
        self.CheckD.grid(row=7,column=0)
        self.CheckD=Checkbutton(Databox,text='Invertir eje X',variable=self.Inv_X,\
            onvalue=True,offvalue=False,command=self.Inertir_X,font=self.fontl)
        self.CheckD.grid(row=8,column=0)

#######################################################
        self.CheckD=Checkbutton(Databox,text='Saltar Calibración',variable=self.SkipCal,\
            onvalue=True,offvalue=False,command=self.SkCal,font=self.fontl)
        self.CheckD.grid(row=9,column=0)
#######################################################
        Label(Databox).grid(row=11,column=0)
        Label(Databox,width=25,bg="#49A").grid(row=12,column=0)

        ButtonBox = Frame(Databox, width="200", height="100",bg="#49A")
        ButtonBox.grid(row=13,column=0)

        Button(ButtonBox,text='ver rango',width=21,
            command=self.Ver,font=self.fontl).grid(row=5,column=0)
        Label(ButtonBox,width=25,bg="#49A").grid(row=6,column=0)

        NexPrev = Frame(ButtonBox,width=200,height=50,bg="#49A")
        NexPrev.grid(row=7,column=0)
        Button(NexPrev,image=self.figL,command=lambda:self.See_Previous(self.xmin,self.xmax)).grid(row=0,column=0)
        Label(NexPrev,width=5,bg="#49A").grid(row=0,column=1)
        Button(NexPrev,image=self.figR,command=lambda:self.See_Next(self.xmin,self.xmax)).grid(row=0,column=2)

        Label(ButtonBox,width=25,bg="#49A").grid(row=8,column=0)
        Button(ButtonBox,text='Deshacer',width=21,
            command=self.Reset,font=self.fontl).grid(row=9,column=0)
        Label(ButtonBox,width=25,bg="#49A").grid(row=10,column=0)    
        Button(ButtonBox,text='Regresar',width=21,
            command=self.Back1,font=self.fontl).grid(row=11,column=0)
        Label(ButtonBox,width=25,bg="#49A").grid(row=12,column=0)
        Button(ButtonBox,text='Continuar',width=21,
            command=self.Next1,font=self.fontl).grid(row=13,column=0)


    def create_framegraficos(self):
        self.framegraficos = Frame(self,bg="cyan")
        self.framegraficos.place(x=220,y=45)
        self.fig = Figure(figsize=(10, 6))
        self.ax1 = self.fig.add_subplot(111)
        self.fig.subplots_adjust(top=0.95,right=0.95,left=0.08,bottom=0.1)

        for f in self.files:
            self.graf_ax0(f,self.xmin,self.xmax)
        self.Set_Ax0()
        self.ax1.set_title(f'{self.Par[26][self.Par[10][1]]}')

        self.fig1 = FigureCanvasTkAgg(self.fig, self.framegraficos)
        self.canvas = FigureCanvasTkAgg(self.fig, self.framegraficos)  # A tk.DrawingArea.
        self.canvas.draw()
        #self.toolbar = NavigationToolbar2Tk(self.canvas, self.framegraficos, pack_toolbar=False)
        #self.toolbar.update()
        #self.toolbar.pack(side='bottom', fill='both')
        self.framegraficos.config(bd=6,relief='groove',cursor='dotbox')
        self.canvas.get_tk_widget().pack(side='top')#, fill='both', expand=1)
        self.span = SpanSelector(self.ax1, self.onselect, 'horizontal', useblit=True,
                rectprops=dict(alpha=0.5, facecolor='tab:red'), span_stays=True)
        self.canvas.mpl_connect('key_press_event', self.span)

    def Set_Ax0(self):
        self.ax1.set_xlabel('Tiempo s',fontproperties=self.fontAxis)
        self.ax1.set_ylabel('Intensidad u.a.',fontproperties=self.fontAxis)
        

    def Inertir_Y(self):
        self.Par[20]=self.Inv_Y.get()
        self.Reset()

    def Inertir_X(self):
        self.Par[19]=self.Inv_X.get()
        self.Reset()

    def SkCal(self):
        self.Par[27]=self.SkipCal.get()

    def onselect(self, xmin, xmax):
        if xmin==xmax:
            pass
        elif (xmax-xmin)<=2*self.step:
            pass
        else:  
            mask = (xmin <= self.x)*(self.x <= xmax) 
            region_x = self.x[mask]
            region_y = self.y[mask]
            self.xmin=xmin
            self.xmax=xmax
            self.write_Entries(region_x[0],region_x[-1])
            if (self.flag==True):
                self.ax1.cla()
                for f in self.files:
                    self.graf_ax0(f,xmin,xmax)
                self.ax1.set_title(f'{self.Par[26][self.Par[10][1]]}')
                self.fig.canvas.draw()
            else:
                self.ax1.cla()
                self.ax1.set_title(f'{name(self.files[self.index]).nam} : {self.Par[26][self.Par[10][1]]}')
                self.graf_ax0(self.files[self.index],xmin,xmax)
            self.fig.canvas.draw()


    def Ver(self):
        xmax=self.Tmax.get()
        xmin=self.Tmin.get()
        if (isfloat(xmax) and isfloat(xmin))==True:
            xmax=float(xmax)
            xmin=float(xmin)
            if xmax<=xmin:
                messagebox.showerror("Error", "Tmax<=Tmin !!")
            elif (xmax-xmin)<=2*self.step:
                messagebox.showwarning("Cuidado", "(Tmax-Tmin) muy pequeño")
            elif (xmin<min(self.x) and xmax>max(self.x)):
                xmin=min(self.x)
                xmax=max(self.x)
                self.write_Entries(xmin,xmax)
            elif xmin<min(self.x):
                xmin=min(self.x)
                self.write_Entries(xmin,xmax)
            elif xmax>max(self.x):
                xmax=max(self.x)
                self.write_Entries(xmin,xmax)
            self.onselect(xmin,xmax) 
        else:
            messagebox.showerror("Error", "Tmax y Tmin deben ser flotantes!!")



    def graf_ax0(self,file,xmin,xmax):
        datos = read_csv(file,header=self.Par[3])
        self.x = datos.values[:,self.Par[10][0]]
        self.y = datos.values[:,self.Par[10][1]]

        #self.x=delete(self.x,0)
        #self.y=delete(self.y,0)
        #for i in range(len(self.x)):
        #    self.x[i]=float(self.x[i])
        #    self.y[i]=float(self.y[i])


        if self.Par[20]==True:
            self.y=Inv_Eje_Y(self.y)
        if self.Par[19]==True:
            self.x=Inv_Eje_X(self.x)
        mask = (xmin <= self.x)*(self.x <= xmax) 
        region_x = self.x[mask]
        region_y = self.y[mask]
        self.ax1.plot(region_x,region_y)



    def write_Entries(self,xmin,xmax):
        self.Tmax.delete(0,END)
        self.Tmax.insert(END,str(xmax))
        self.Tmin.delete(0,END)
        self.Tmin.insert(END,str(xmin))


    def Reset(self):
        self.flag=True
        self.index=-1
        self.Op_files()
        self.ax1.cla()
        for f in self.files:
            self.graf_ax0(f,self.xmin,self.xmax)

        self.ax1.set_title(f'{self.Par[26][self.Par[10][1]]}')

        self.fig.canvas.draw()
        self.write_Entries(self.xmin,self.xmax)

    def Op_files(self):
        self.files = glob(self.Par[2])
        datos = read_csv(self.files[0],header=self.Par[3])
        self.x = datos.values[:,self.Par[10][0]]

        #self.x=delete(self.x,0)
        #for i in range(len(self.x)):
        #    self.x[i]=float(self.x[i])

        self.step = self.x[1]-self.x[0]#######MODIFY
        self.xmax=max(self.x)
        self.xmin=min(self.x)


    def See_Next(self,xmin,xmax):
        self.flag=False
        self.index=self.index+1
        if self.index>=len(self.files):
            self.index=0
        self.ax1.cla()
        self.ax1.set_title(f'{name(self.files[self.index]).nam} : {self.Par[26][self.Par[10][1]]}')
        self.graf_ax0(self.files[self.index],self.xmin,self.xmax)
        self.fig.canvas.draw()

    def See_Previous(self,xmin,xmax):
        self.flag=False
        self.index=self.index-1
        if self.index<=-len(self.files):
            self.index=0
        self.ax1.cla()
        self.ax1.set_title(f'{name(self.files[self.index]).nam} : {self.Par[26][self.Par[10][1]]}')
        self.graf_ax0(self.files[self.index],self.xmin,self.xmax)
        self.fig.canvas.draw()



    def Next1(self):
        self.Par[4]=self.files
        a=[self.xmax,self.xmin]
        self.Par[5]=a
        close('all')
        if self.Par[27]==0:
            self.master.switch_frame(WinCal,self.Par)
        else:
            self.master.switch_frame(WinGauss,self.Par)
        

    def Back1(self):
        self.Par[10]=2
        self.Par[19]=False
        self.Par[20]=False
        close('all')
        #self.master.destroy()



######################################################
# VEntana de Calibración
from Config1 import Transicion
from Cal_Clas1 import Calibracion
from matplotlib.widgets import Cursor
from matplotlib.backend_bases import MouseButton

#from FGauss_GUI2 import WinGauss
#from Fit_GUI1 import WinFit
#######################################################

class WinCal(Frame):
    def __init__(self, master=None,Par=None):
        super().__init__(master,width="1240", height="680",bg="#49A")
        self.Par=Par
        self.fontT=self.master.fontT
        self.fontl=self.master.fontl
        self.fontAxis=self.master.fontAxis
        self.master = master
        self.x = []
        self.y = []
        self.xmax=Par[5][0]
        self.xmin=Par[5][1]
        self.ax1 = None
        self.files = Par[4]
        self.flag0 = IntVar() # Habilita checkbutton, inicia selección de dips
        self.Metodo= IntVar()
        self.flag = False # Flag origen del ajuste. False-> Boton ajuste, True-> botón analizar todos.
        self.flag1 = True #Asociada a flag0
        self.flag2 = False # True indica que se han seleccionado los 6 dips
        self.flagFGauss = True #Flag EStoy en la ventana: True->Estoy en la ventana de ajuste de fondo gaussiano
        self.Cursor=None
        self.click=None
        self.index=0
        self.findex = 0
        self.px=[]
        self.lb_in=[]
        self.config=Transicion(self.Par)
        self.figR=PhotoImage(file='nextFig.png')
        self.figL=PhotoImage(file='prevFig.png')
        self.pack(side='top')
        self.create_Databox()
        self.create_framegraficos()
        self.EstadoFlag()       

    def create_Databox(self):
        name=self.config.Name

        Label(self,text='Calibración: '+name,
            bg="#49A",font=self.fontT).place(x=500,y=10)

        Databox = Frame(self, width="200", height="600")
        Databox.place(x=20,y=5)

        Label(Databox).grid(row=0,column=0)
        self.CheckD=Checkbutton(Databox,text='Seleccionar Dips',variable=self.flag0,\
            onvalue=True,offvalue=False,command=self.EstadoFlag)
        self.CheckD.grid(row=1,column=0)
        Label(Databox).grid(row=2,column=0)

        Dips = Frame(Databox, width="200", height="200")
        Dips.grid(row=3,column=0)
        for i in range(len(self.config.HS)):
            self.lb_in.append(0)
            self.px.append(0)
            Label(Dips,text=self.config.HS[i],font=self.fontl).grid(row=i,column=0)
            self.lb_in[i]=Entry(Dips,width=20,font=self.fontl)
            self.lb_in[i].grid(row=i,column=1)
        Label(Dips,text='w',font=self.fontl).grid(row=i+1,column=0)
        self.w=Entry(Dips,width=20,font=self.fontl)
        self.w.grid(row=i+1,column=1)

        Label(Databox,width=25).grid(row=4,column=0)
        Label(Databox,text='Fmax [MHz]',font=self.fontl).grid(row=5,column=0)
        self.Fmax=Entry(Databox,width=20,font=self.fontl)
        self.Fmax.grid(row=6,column=0)
        Label(Databox,width=25).grid(row=7,column=0)
        Label(Databox,text='Fmin [MHz]',font=self.fontl).grid(row=8,column=0)
        self.Fmin=Entry(Databox,width=20,font=self.fontl)
        self.Fmin.grid(row=9,column=0)
        Label(Databox,width=25).grid(row=10,column=0)

        sel=Radiobutton(Databox,text="Método 1",variable=self.Metodo,value=1)
        sel.select()
        sel.grid(row=11,column=0)
        Radiobutton(Databox,text="Método 2",variable=self.Metodo,
            value=2).grid(row=12,column=0)
        #Label(Databox).grid(row=13,column=0)
        Label(Databox,width=25,bg="#49A").grid(row=13,column=0) 

        ButtonBox = Frame(Databox, width="200", height="100",bg="#49A")
        ButtonBox.grid(row=14,column=0) 

        Button(ButtonBox,text='Reestablecer Dips',width=21,
            command=self.Res_Deeps,font=self.fontl).grid(row=0,column=0)
        Label(ButtonBox,width=25,bg="#49A").grid(row=1,column=0)    
        self.Cal=Button(ButtonBox,text='Calibrar',width=21,
            command=lambda:self.Check_Entries(self.files[self.findex]),font=self.fontl)
        self.Cal['state']='normal'
        self.Cal.grid(row=2,column=0)
        Label(ButtonBox,width=25,bg="#49A").grid(row=3,column=0)

        NexPrev = Frame(ButtonBox,width=200,height=50,bg="#49A")
        NexPrev.grid(row=4,column=0)
        Button(NexPrev,image=self.figL,command=self.See_Previous).grid(row=0,column=0)
        Label(NexPrev,width=5,bg="#49A").grid(row=0,column=1)
        Button(NexPrev,image=self.figR,command=self.See_Next).grid(row=0,column=2)

        Label(ButtonBox,width=25,bg="#49A").grid(row=8,column=0)
        Button(ButtonBox,text='Regresar',width=21,
            command=self.Back1,font=self.fontl).grid(row=9,column=0)
        Label(ButtonBox,width=25,bg="#49A").grid(row=10,column=0)
        self.Cont=Button(ButtonBox,text='Continuar',width=21,
            command=self.Next1,font=self.fontl)
        self.Cont['state']='disable'
        self.Cont.grid(row=11,column=0)


    def create_framegraficos(self):
        self.framegraficos = Frame(self,bg="cyan")
        self.framegraficos.place(x=220,y=45)
        self.fig = Figure(figsize=(11, 6),dpi=90)
        self.ax1 = self.fig.add_subplot(111)
        self.fig.subplots_adjust(top=0.95,right=0.95,left=0.08,bottom=0.1)

        self.graf_ax0(self.files[0],self.xmin,self.xmax)
        self.Set_Ax0()

        self.fig1 = FigureCanvasTkAgg(self.fig, self.framegraficos)
        self.canvas = FigureCanvasTkAgg(self.fig, self.framegraficos)  # A tk.DrawingArea.
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.framegraficos, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side='bottom', fill='both')
        self.framegraficos.config(bd=6,relief='groove')
        self.canvas.get_tk_widget().pack(side='top')#, fill='both', expand=1)

    def Set_Ax1(self):
        #self.ax1.set_xlabel('Frecuencia MHz',fontproperties=self.fontAxis)
        #self.ax1.set_ylabel('Intensidad u.a.',fontproperties=self.fontAxis)
        self.ax1.set_xlabel(r'$\delta$ (MHz)',fontproperties=self.fontAxis)
        self.ax1.set_ylabel('Fluorescencia (u.a.)',fontproperties=self.fontAxis)

    def Set_Ax0(self):
        #self.ax1.set_xlabel('Tiempo s',fontproperties=self.fontAxis)
        #self.ax1.set_ylabel('Intensidad u.a.',fontproperties=self.fontAxis)
        self.ax1.set_xlabel(r'Tiempo (s)',fontproperties=self.fontAxis)
        self.ax1.set_ylabel('Fluorescencia (u.a.)',fontproperties=self.fontAxis)

    def Res_Deeps(self):
        for i in range(len(self.config.HS)):
            self.write_Entrie(self.lb_in[i],0)
            self.px[i]=0
        self.CheckD.select()
        self.Cal['state']='normal' ####### #################
        self.Cont['state']='disable'
        self.flag2=False
        self.ax1.cla()
        self.ax1.set_title(f'{name(self.files[self.findex]).nam}')
        self.graf_ax0(self.files[self.findex],self.xmin,self.xmax)
        self.Set_Ax0()
        self.fig.canvas.draw()
        self.EstadoFlag()
        

    def Check_Entries(self,file):
        if sum(self.px)==0:
            for i in range(len(self.config.HS)):
                self.px[i]=self.lb_in[i].get()
                if isfloat(self.px[i])==False:
                    messagebox.showerror("Error", f"{self.config.HS[i]} invalido!! \n Debe ser un flotante")
                    for i in range(len(self.config.HS)):
                        self.px[i]=0
                    return 0
                else:
                    self.px[i]=float(self.px[i])

        self.Par[6]=self.px

        w=self.w.get()
        if w.isdigit()==False:
            messagebox.showerror("Error", "W invalido!! \n Debe ser un entero")
            return 0
        else:
            self.Par[7]=int(w)

        Fmax=self.Fmax.get()
        if isfloat(Fmax)==False:
            messagebox.showerror("Error", "Fmax invalido!! \n Debe ser un Flotante")
            return 0
        else:
            self.Par[24]=float(Fmax)

        Fmin=self.Fmin.get()
        if isfloat(Fmin)==False:
            messagebox.showerror("Error", "Fmin invalido!! \n Debe ser un Flotante")
            return 0
        else:
            self.Par[25]=float(Fmin)

        if self.Par[25]>=self.Par[24]:
            messagebox.showerror("Error", "Fmin debe ser estrictamente menor que Fmax!!")
            return 0

        self.Par[11]=self.Metodo.get()
        self.Calibrar(file)
        

    def Calibrar(self,file):
        self.Par[17]=True
        self.Par[18]=''
        x=Calibracion(self.Par,file)
        if self.Par[11]==1:
            try:
                #x.Cal2()
                x.Cal()
            except:
                if self.flag==False:
                    messagebox.showerror('Error','Este archivo no se puede calibrar con el método seleccionado.')
                else:
                    self.Par[18]='Calibración'
                return 0
        elif self.Par[11]==2:
            try:
                x.Cal1()
            except:
                if self.flag==False:
                    messagebox.showerror('Error','Este archivo no se puede calibrar con el método seleccionado.')
                else:
                    self.Par[18]='Calibración'
                return 0
        self.frec=x.frec
        self.volt=x.Volt
        mask1 = (self.Par[25] < self.frec)*(self.frec < self.Par[24])
        self.frec = self.frec[mask1] 
        self.volt = self.volt[mask1]

        if self.flagFGauss==False:
            if self.Par[1]!=4:
                try:
                    self.FG=FGauss(self.Par,self.frec,self.volt)
                    self.volt=self.FG.SubDoppler
                except:
                    if self.flag==False:
                        messagebox.showerror('Error','Este archivo no se pudo ajustar el fondo Gaussiano.')
                    else:
                        self.Par[18]='Fondo Gaussiano'
                    return 0

        if self.flag==False:
            self.ax1.cla()
            self.graf_ax1()
            self.Set_Ax1()
            self.fig.canvas.draw()
            self.Cont['state']='normal'
            self.Cal['state']='normal' ###### #############

    def graf_ax1(self):
        #self.ax1.plot(self.frec,self.volt,linestyle='-')
        self.ax1.plot(self.frec,self.volt,linestyle='-')
        #self.ax1.axhline(y=0, color='black', linestyle='dotted')
        self.ax1.set_title(f'{name(self.files[self.findex]).nam} : {self.Par[26][self.Par[10][1]]}')
        


    def EstadoFlag(self):
        if self.flag0.get()==True:
            self.flag1=True
            self.index=0
            self.Selec_Deeps()
        else:
            self.flag1=False
            self.Cursor=0
            self.canvas.mpl_disconnect(self.click)
            for i in range(len(self.config.HS)):
                self.lb_in[i]['state']='normal' ##### ###########



    def Selec_Deeps(self):
        self.Cursor=Cursor(self.ax1,vertOn=True,horizOn=False, useblit=False, color='red', linewidth=1)
        self.click=self.canvas.mpl_connect('button_press_event', self.on_click)
        

    def write_Entrie(self,en,x):
        en['state']='normal'
        en.delete(0,END)
        en.insert(END,str(x))
        en['state']='normal'  ##### ############### 


    def Get_Click(self,i,x):
        self.px[i]=x
        self.write_Entrie(self.lb_in[i],x)
        #self.ax1.axvline(x=x, color='red', linestyle='dotted')
        self.ax1.axvline(x=x, color='red', linestyle='dotted',linewidth=2)

        #self.ax1.text(x,max(self.y),s=self.config.HS[i],fontproperties=self.fontAxis, rotation='vertical',ha='right',va='center')
        self.ax1.text(x-0.00003,max(self.y),s=self.config.HS[i],fontsize=15, rotation='vertical',ha='right',va='center')
        
        self.fig.canvas.draw()
        if self.index==(len(self.config.HS)-1):
            self.flag2=True
            self.CheckD.deselect()
            self.Cal['state']='normal'
            self.EstadoFlag()
        

    def on_click(self,event):
        if self.index<=(len(self.config.HS)):
            if event.button is MouseButton.LEFT:
                x = event.x
            if event.inaxes:
                self.ax1 = event.inaxes
                self.Get_Click(self.index,event.xdata)
                self.index=self.index+1

    def graf_ax0(self,file,xmin,xmax):
        datos = read_csv(file,header=self.Par[3])
        self.x = datos.values[:,self.Par[10][0]]
        self.y = datos.values[:,self.Par[10][1]]
        if self.Par[20]==True:
            self.y=Inv_Eje_Y(self.y)
        if self.Par[19]==True:
            self.x=Inv_Eje_X(self.x)
        mask = (xmin <= self.x)*(self.x <= xmax) 
        region_x = self.x[mask]
        region_y = self.y[mask]
        self.ax1.plot(region_x,region_y)
        self.ax1.set_title(f'{name(file).nam} : {self.Par[26][self.Par[10][1]]}')


    
    def See_Next(self):
        self.CheckD.deselect()
        self.Cursor=0
        self.canvas.mpl_disconnect(self.click)
        if self.flag2:
            self.Cal['state']='normal'
        else:
            self.CheckD.deselect()
            self.Cursor=0
            self.canvas.mpl_disconnect(self.click)

        self.findex=self.findex+1
        if self.findex>=len(self.files):
            self.findex=0
        self.ax1.cla()
        self.ax1.set_title(f'{name(self.files[self.findex]).nam}')
        self.graf_ax0(self.files[self.findex],self.xmin,self.xmax)
        self.Set_Ax0()
        self.fig.canvas.draw()

    def See_Previous(self):
        self.CheckD.deselect()
        self.Cursor=0
        self.canvas.mpl_disconnect(self.click)
        if self.flag2:
            self.Cal['state']='normal'
        else:
            self.CheckD.deselect()
            self.Cursor=0
            self.canvas.mpl_disconnect(self.click)

        self.findex=self.findex-1
        if self.findex<=-len(self.files):
            self.findex=0
        self.ax1.cla()
        self.ax1.set_title(f'{name(self.files[self.findex]).nam}')
        self.graf_ax0(self.files[self.findex],self.xmin,self.xmax)
        self.Set_Ax0()
        self.fig.canvas.draw()


    def Next1(self):
        a=self.Metodo.get()
        self.Par[11]=a
        close('all')
        if self.Par[1]==4:
            self.master.switch_frame(WinFit,self.Par)
        else:    
            self.master.switch_frame(WinGauss,self.Par)


    def Back1(self):
        close('all')
        self.master.switch_frame(WinRango,self.Par)
        #self.master.destroy()

########################################################################
#Ventana de ajuste de fondo Gaussiano

from tkinter import PhotoImage
from Doppler import DopplerW
from FGauss_Class import FGauss

#######################################################

class WinGauss(Frame):
    def __init__(self, master=None,Par=None):
        super().__init__(master,width="1240", height="680",bg="#49A")
        self.Par=Par
        self.fontT=self.master.fontT
        self.fontl=self.master.fontl
        self.fontAxis=self.master.fontAxis
        self.LegSize=self.master.LegSize
        self.master = master
        self.x = []
        self.y = []
        self.frec=[]
        self.volt=[]
        self.xmax=Par[5][0]
        self.xmin=Par[5][1]
        self.ax1 = None
        self.files = Par[4]
        self.findex = 0
        self.flag = False# Flag origen del ajuste. False-> Boton ajuste, True-> botón analizar todos.
        self.flagFGauss = True #Flag EStoy en la ventana: True->Estoy en la ventana de ajuste de fondo gaussiano
        self.figR=PhotoImage(file='nextFig.png')
        self.figL=PhotoImage(file='prevFig.png')
        self.px=[0,0,0,0,0,0]
        self.config=Transicion(self.Par)
        self.pack(side='top')
        self.create_Databox()
        self.create_framegraficos()       

    def create_Databox(self):
        name=self.config.Name

        Label(self,text='Fondo Gaussiano: '+name,
            bg="#49A",font=self.fontT).place(x=500,y=10)

        Databox = Frame(self, width="200", height="600")
        Databox.place(x=20,y=45)

        Label(Databox).grid(row=0,column=0)

        Label(Databox,text='T [K]',font=self.fontl).grid(row=1,column=0)
        self.T=Entry(Databox,width=20,font=self.fontl)
        self.T.grid(row=2,column=0)
        Label(Databox).grid(row=3,column=0)
        Label(Databox,text='FWHM [MHz]',font=self.fontl).grid(row=4,column=0)
        self.W=Entry(Databox,width=20,font=self.fontl,state='disable')
        self.W.grid(row=5,column=0)
        Label(Databox).grid(row=6,column=0)
        Label(Databox,width=25,bg="#49A").grid(row=7,column=0)

        ButtonBox = Frame(Databox, width="200", height="100",bg="#49A")
        ButtonBox.grid(row=8,column=0)     
        self.B_Ajus=Button(ButtonBox,text='Ajustar',width=21,
            command=self.Ajustar,font=self.fontl)
        self.B_Ajus.grid(row=1,column=0)        
        Label(ButtonBox,width=25,bg="#49A").grid(row=2,column=0) 
        self.Borrar=Button(ButtonBox,text='Borrar',width=21,
            command=self.Borrar,font=self.fontl)
        self.Borrar.grid(row=3,column=0)
        Label(ButtonBox,width=25,bg="#49A").grid(row=4,column=0)   
        self.B_Res=Button(ButtonBox,text='Restar',width=21,
            command=self.Restar,font=self.fontl)
        self.B_Res['state']='disable'
        self.B_Res.grid(row=5,column=0)
        Label(ButtonBox,width=25,bg="#49A").grid(row=6,column=0)

        NexPrev = Frame(ButtonBox,width=200,height=50,bg="#49A")
        NexPrev.grid(row=7,column=0)
        Button(NexPrev,image=self.figL,command=self.See_Previous).grid(row=0,column=0)
        Label(NexPrev,width=5,bg="#49A").grid(row=0,column=1)
        Button(NexPrev,image=self.figR,command=self.See_Next).grid(row=0,column=2)

        Label(ButtonBox,width=25,bg="#49A").grid(row=8,column=0)
        Button(ButtonBox,text='Regresar',width=21,
            command=self.Back1,font=self.fontl).grid(row=9,column=0)
        Label(ButtonBox,width=25,bg="#49A").grid(row=10,column=0)
        self.Cont=Button(ButtonBox,text='Continuar',width=21,
            command=self.Next1,font=self.fontl)
        self.Cont['state']='disable'
        self.Cont.grid(row=11,column=0)


    def create_framegraficos(self):
        self.framegraficos = Frame(self,bg="cyan")
        self.framegraficos.place(x=220,y=45)
        self.fig = Figure(figsize=(11, 6),dpi=90)
        self.ax1 = self.fig.add_subplot(111)
        self.fig.subplots_adjust(top=0.95,right=0.95,left=0.08,bottom=0.1)

        self.Calibrar(self.files[0])
        self.Set_Ax1()


        self.fig1 = FigureCanvasTkAgg(self.fig, self.framegraficos)
        self.canvas = FigureCanvasTkAgg(self.fig, self.framegraficos)  # A tk.DrawingArea.
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.framegraficos, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side='bottom', fill='both')
        self.framegraficos.config(bd=6,relief='groove')
        self.canvas.get_tk_widget().pack(side='top')#, fill='both', expand=1)

    def Set_Ax1(self):
        #self.ax1.set_xlabel('Frecuencia MHz',fontproperties=self.fontAxis)
        #self.ax1.set_ylabel('Intensidad u.a.',fontproperties=self.fontAxis)
        self.ax1.set_xlabel(r'$\delta$ (MHz)',fontproperties=self.fontAxis)
        self.ax1.set_ylabel('Fluorescencia (u.a.)',fontproperties=self.fontAxis)

    def Ajustar(self):
        T=self.T.get()
        if isfloat(T)==False:
            messagebox.showerror("Error", "T invalido!!")
            return 0
        elif float(T)<=0:
            messagebox.showerror("Error", "T invalido!!")
            return 0
        else:
            self.Par[8]=float(T)
        FWHM=DopplerW(self.Par).FWHM
        self.Par[9]=FWHM
        self.W['state']='normal'
        self.W.delete(0,END)
        self.W.insert(END,str(FWHM))
        self.W['state']='disable'
        self.FG=FGauss(self.Par,self.frec,self.volt)
        self.ax1.plot(self.frec,self.FG.GausFit3,linestyle='dashed',\
            label=f'T={self.Par[8]} K',linewidth=3)
        self.ax1.legend(loc='best', shadow=True, fontsize=self.LegSize)
        self.fig.canvas.draw()
        self.B_Res['state']='normal'
        self.Cont['state']='normal'
        self.Borrar['state']='normal'

    def Restar(self):
        self.ax1.cla()
        self.ax1.set_title(f'{name(self.files[self.findex]).nam}')
        self.ax1.plot(self.frec,self.FG.SubDoppler,label=f'T={self.Par[8]} K')
        self.ax1.legend(loc='best', shadow=True, fontsize=10)
        self.ax1.axhline(y=0, color='black', linestyle='dotted')
        self.fig.canvas.draw()    
        self.B_Ajus['state']='disable'  
        self.Borrar['state']='disable'  


    def Borrar(self):
        self.B_Res['state']='disable'
        self.B_Ajus['state']='normal'
        self.Cont['state']='disable'
        self.ax1.cla()
        self.ax1.set_title(f'{name(self.files[self.findex]).nam}')
        self.Calibrar(self.files[self.findex])
        self.Set_Ax1()
        self.fig.canvas.draw()


    def Calibrar(self,file):
        self.Par[17]=True
        self.Par[18]=''
        x=Calibracion(self.Par,file)
        if self.Par[11]==1:
            try:
                x.Cal()
            except:
                if self.flag==False:
                    messagebox.showerror('Error','Este archivo no se puede calibrar con el método seleccionado.')
                else:
                    self.Par[18]='Calibración'
                return 0
        elif self.Par[11]==2:
            try:
                x.Cal1()
            except:
                if self.flag==False:
                    messagebox.showerror('Error','Este archivo no se puede calibrar con el método seleccionado.')
                else:
                    self.Par[18]='Calibración'
                return 0

        self.frec=x.frec 
        self.volt=x.Volt

        if self.Par[27]==1:
            self.Par[25]=min(self.frec)
            self.Par[24]=max(self.frec)
        #################################################################
        mask1 = (self.Par[25] < self.frec)*(self.frec < self.Par[24])
        self.frec = self.frec[mask1] 
        self.volt = self.volt[mask1]

        if self.flagFGauss==False:
            if self.Par[1]!=4:
                try:
                    self.FG=FGauss(self.Par,self.frec,self.volt)
                    self.volt=self.FG.SubDoppler
                except:
                    if self.flag==False:
                        messagebox.showerror('Error','Este archivo no se pudo ajustar el fondo Gaussiano.')
                    else:
                        self.Par[18]='Fondo Gaussiano'
                    return 0

        if self.flag==False:
            self.graf_ax1()

    def graf_ax1(self):
        self.ax1.plot(self.frec,self.volt,linestyle='-')
        #self.ax1.axhline(y=0, color='black', linestyle='dotted')
        self.ax1.set_title(f'{name(self.files[self.findex]).nam} : {self.Par[26][self.Par[10][1]]}')

    def See_Next(self):
        self.B_Ajus['state']='normal'
        self.B_Res['state']='disable'
        self.findex=self.findex+1
        if self.findex>=len(self.files):
            self.findex=0
        self.ax1.cla()
        #self.ax1.set_title(f'{name(self.files[self.findex]).nam}')
        self.Calibrar(self.files[self.findex])
        self.Set_Ax1()
        self.fig.canvas.draw()

    def See_Previous(self):
        self.B_Ajus['state']='normal'
        self.B_Res['state']='disable'
        self.findex=self.findex-1
        if self.findex<=-len(self.files):
            self.findex=0
        self.ax1.cla()
        self.Set_Ax1()
        #self.ax1.set_title(f'{name(self.files[self.findex]).nam}')
        self.Calibrar(self.files[self.findex])
        self.fig.canvas.draw()


    def Next1(self):
        close('all')
        self.master.switch_frame(WinFit,self.Par)


    def Back1(self):
        close('all')
        self.master.switch_frame(WinCal,self.Par)


#####################################################################
# Ventana de ajustes perfiles Sub-Doppler
from tkinter import Toplevel
from numpy import std, corrcoef 

from Lorentz_Class1 import LorentzFit
from Voigt_Class import VoigtFit
from Gauss_Class import GaussFit
from Write_Result import InitWrite, WriteDataFit, WriteEspectro,\
    WriteReport, Make_Labels, Centros, Widths

#######################################################
class WinFit(Frame):
    def __init__(self, master=None,Par=None):
        super().__init__(master,width="1240", height="680",bg="#49A")
        self.Par=Par
        self.fontT=self.master.fontT
        self.fontl=self.master.fontl
        self.fontAxis=self.master.fontAxis
        self.LegSize=self.master.LegSize
        self.master = master
        self.x = []
        self.y = []
        self.frec=[]
        self.volt=[]
        self.xmax=Par[5][0]
        self.xmin=Par[5][1]
        self.ax1 = None
        self.files = Par[4]
        self.findex = 0
        self.flag = False # Flag origen del ajuste. False-> Boton ajuste, True-> botón analizar todos.
        self.flagFGauss = False #Flag EStoy en la ventana: True->Estoy en la ventana de ajuste de fondo gaussiano
        self.config=Transicion(self.Par)
        self.popt=None
        self.perr=None
        self.modelType=None
        self.model_Fit=None
        self.voigt_flag=IntVar()
        self.figR=PhotoImage(file='nextFig.png')
        self.figL=PhotoImage(file='prevFig.png')
        self.pack(side='top')
        self.create_Databox()
        self.create_framegraficos()       

    def create_Databox(self):
        name=self.config.Name

        Label(self,text='Ajuste de HFS: '+name,\
            bg="#49A",font=self.fontT).place(x=500,y=10)

        Databox = Frame(self, width="200", height="600")
        Databox.place(x=20,y=5)

        Label(Databox).grid(row=0,column=0)

        Label(Databox,text='LW min [MHz]',font=self.fontl).grid(row=1,column=0)
        self.Wmin=Entry(Databox,width=20,font=self.fontl)
        self.Wmin.grid(row=2,column=0)
        Label(Databox).grid(row=3,column=0)
        Label(Databox,text='LW max [MHz]',font=self.fontl).grid(row=4,column=0)
        self.Wmax=Entry(Databox,width=20,font=self.fontl)
        self.Wmax.grid(row=5,column=0)
        Label(Databox).grid(row=6,column=0)
        Label(Databox,text='Gsig min [MHz]',font=self.fontl).grid(row=7,column=0)
        self.Gmin=Entry(Databox,width=20,font=self.fontl)
        self.Gmin.grid(row=8,column=0)
        Label(Databox).grid(row=9,column=0)
        Label(Databox,text='Gsig max [MHz]',font=self.fontl).grid(row=10,column=0)
        self.Gmax=Entry(Databox,width=20,font=self.fontl)
        self.Gmax.grid(row=11,column=0)
        Label(Databox).grid(row=12,column=0)
        Label(Databox,text='dC [MHz]',font=self.fontl).grid(row=13,column=0)
        self.dC=Entry(Databox,width=20,font=self.fontl)
        self.dC.grid(row=14,column=0)

        Label(Databox).grid(row=15,column=0)
        self.voigt_check=Checkbutton(Databox,text='Mismo Lorentz w',variable=self.voigt_flag,\
            onvalue=True,offvalue=False,font=self.fontl)
        self.voigt_check.grid(row=16,column=0)
        #Label(Databox).grid(row=17,column=0)

        Label(Databox,width=25,bg="#49A").grid(row=18,column=0) 

        ButtonBox = Frame(Databox, width="200", height="100",bg="#49A")
        ButtonBox.grid(row=19,column=0)      
        self.B_Ajus=Button(ButtonBox,text='Ajustar',width=21,
            command=self.Check_Cotas,font=self.fontl)
        self.B_Ajus.grid(row=1,column=0)        
        Label(ButtonBox,width=25,bg="#49A").grid(row=2,column=0) 
        Button(ButtonBox,text='Borrar',width=21,
            command=self.Borrar,font=self.fontl).grid(row=3,column=0)
        Label(ButtonBox,width=25,bg="#49A").grid(row=4,column=0)
        Button(ButtonBox,text='Info Ajuste',width=21,
            command=self.WinInfo,font=self.fontl).grid(row=5,column=0)
        Label(ButtonBox,width=25,bg="#49A").grid(row=6,column=0)

        NexPrev = Frame(ButtonBox,width=200,height=50,bg="#49A")
        NexPrev.grid(row=7,column=0)
        Button(NexPrev,image=self.figL,command=self.See_Previous).grid(row=0,column=0)
        Label(NexPrev,width=5,bg="#49A").grid(row=0,column=1)
        Button(NexPrev,image=self.figR,command=self.See_Next).grid(row=0,column=2)

        Label(ButtonBox,width=25,bg="#49A").grid(row=8,column=0)
        self.B_Analizar=Button(ButtonBox,text='Analizar Todos',width=21,
            command=self.Analizar,font=self.fontl)
        self.B_Analizar.grid(row=9,column=0)
        self.B_Analizar['state']='disable'
        Label(ButtonBox,width=25,bg="#49A").grid(row=10,column=0)
        Button(ButtonBox,text='Regresar',width=21,
            command=self.Back1,font=self.fontl).grid(row=11,column=0)
        #Label(ButtonBox,width=25,bg="#49A").grid(row=12,column=0)


    def create_framegraficos(self):
        self.framegraficos = Frame(self,bg="cyan")
        self.framegraficos.place(x=220,y=45)
        self.fig = Figure(figsize=(11, 6),dpi=90)
        self.ax1 = self.fig.add_subplot(111)
        self.fig.subplots_adjust(top=0.95,right=0.95,left=0.08,bottom=0.1)

        self.Calibrar(self.files[0])
        self.Set_Ax1()

        self.fig1 = FigureCanvasTkAgg(self.fig, self.framegraficos)
        self.canvas = FigureCanvasTkAgg(self.fig, self.framegraficos)  # A tk.DrawingArea.
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.framegraficos, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side='bottom', fill='both')
        self.framegraficos.config(bd=6,relief='groove')
        self.canvas.get_tk_widget().pack(side='top')#, fill='both', expand=1)


    def WinInfo(self):
        if self.popt is None:
            return 0
        else:
            labs=Make_Labels(self.config,self.modelType)
            popt,perr=Centros(self.popt,self.perr,self.config.Trans,self.Par[1])
            popt,perr=Widths(popt,perr,self.config.Trans,self.modelType,self.Par[1])
            info=Toplevel(self)
            info.title('Datos de Ajuste')
            Label(info,text=f'Modelo: {self.modelType}').grid(row=0,column=1)
            Label(info,text=f'Archivo: {name(self.files[self.findex]).nam}').grid(row=0,column=3)
            j=1
            for i in range(len(self.popt)):
                if j==1:
                    color='white'
                else:
                    color='#8FE994'
                Label(info,text=f'{labs[i]}=',width=15,bg=color).grid(row=i+1,column=0)
                Label(info,text=f'{popt[i]}',width=25,bg=color).grid(row=i+1,column=1)
                Label(info,text='+-',width=2,bg=color).grid(row=i+1,column=2)
                Label(info,text=f'{perr[i]}',width=25,bg=color).grid(row=i+1,column=3)
                j*=-1


    def Set_Ax1(self):
        #self.ax1.set_xlabel('Frecuencia MHz',fontproperties=self.fontAxis)
        #self.ax1.set_ylabel('Intensidad u.a.',fontproperties=self.fontAxis)
        self.ax1.set_xlabel(r'$\delta$ (MHz)',fontproperties=self.fontAxis)
        self.ax1.set_ylabel('Fluorescencia (u.a.)',fontproperties=self.fontAxis)
        self.ax1.ticklabel_format(axis='y', style='sci',scilimits=(-2,2))

    def Analizar(self):
        self.B_Analizar['bg']='yellow'
        self.flag=True
        popt=self.popt
        perr=self.perr
        ruta = (self.Par[2][:self.Par[2].rfind("*")])+'Resultados'
#######################
        try:
            Data_Fit,Report=InitWrite(self.modelType,self.config,self.Par)
        except:
            messagebox.showerror('Error','Cierra todos los archivos e intenta de nuevo.')
            return 0
#######################
        for f in self.files:
            self.Calibrar(f)
            if self.Par[17]==True: 
                self.Ajustar()
            WriteReport(name(f).nam,self.Par[17],self.Par[18],Report)
            if self.Par[17]==True:
                WriteDataFit(name(f).nam,self.popt,self.perr,Data_Fit,self.config.Trans,self.modelType,self.Par[1])
#######################                
                try:
                    #WriteEspectro(name(f).nam,self.frec,self.volt-self.popt[-1],self.model_Fit-self.popt[-1],ruta)
                    WriteEspectro(name(f).nam,self.frec,self.VEsp,self.volt,self.model_Fit,ruta)
                except:
                    messagebox.showerror('Error','Cierra todos los archivos e intenta de nuevo.')
                    return 0
#######################
        Data_Fit.close()
        Report.close()
        self.popt=popt
        self.perr=perr
        self.B_Analizar['bg']='green'
        self.flag=False



    def Check_Cotas(self):
        wmin=0
        wmax=0
        Gmin=0
        Gmax=0
        dC=0
        entradas=[self.Wmin,self.Wmax,self.Gmin,self.Gmax,self.dC]
        salidas=[wmin,wmax,Gmin,Gmax,dC]
        lab=['W min','W max','G min','G max','dC']
        for i in range(len(entradas)):
            salidas[i]=entradas[i].get()
            if isfloat(salidas[i])==False:
                messagebox.showerror("Error", f'{lab[i]} invalido!!')
                return 0
            elif float(salidas[0])<0:
                messagebox.showerror("Error", f'{lab[i]} invalido!!')
                return 0
            elif float(salidas[0])<float(salidas[1])<0:
                messagebox.showerror("Error", f'{lab[i]} invalido!!')
                return 0
            else:
                self.Par[12+i]=float(salidas[i])
        self.Model()

    def Model(self):
        Gmax=self.Par[15]
        wmax=self.Par[13]
        if Gmax==0:
            self.modelType='Lorentz'
        elif wmax==0:
            self.modelType='Gauss'
        else:
            if self.voigt_flag.get()==False:
                self.modelType='Voigt'
                self.Par[21]=False
            elif self.voigt_flag.get()==True:
                self.modelType='Voigt_1L'
                self.Par[21]=True
        self.Ajustar()


    def Ajustar(self):
        modelType=self.modelType
        self.Par[17]=True
        self.Par[18]=''

        if modelType=='Lorentz':
            fit=LorentzFit(self.Par,self.frec,self.volt)
            try:
                if self.Par[1]==4:
                    self.popt, self.perr=fit.L_Fit3()
                    model=fit.lorentz3(self.frec,*self.popt)
                else:
                    self.popt, self.perr=fit.L_Fit6()
                    model=fit.lorentz6(self.frec,*self.popt)
            except:
                if self.flag==False:
                    messagebox.showerror("Error", 'No se pudo ajustar, modifica los parámetros.')
                    return 0
                else:
                    self.Par[17]=False
                    self.Par[18]='Ajuste'
                #return 0

        elif modelType=='Gauss':
            fit=GaussFit(self.Par,self.frec,self.volt)
            try:
                if self.Par[1]==4:
                    self.popt, self.perr=fit.G_Fit3()
                    model=fit.gauss3(self.frec,*self.popt)
                else:
                    self.popt, self.perr=fit.G_Fit6()
                    model=fit.gauss6(self.frec,*self.popt)
            except:
                if self.flag==False:
                    messagebox.showerror("Error", 'No se pudo ajustar, modifica los parámetros.')
                    return 0
                else:
                    self.Par[17]=False
                    self.Par[18]='Ajuste'
                #return 0

        elif modelType=='Voigt_1L':
            fit=VoigtFit(self.Par,self.frec,self.volt)
            #self.popt, self.perr=fit.V_Fit31L()
            #model=fit.Voigt31L(self.frec,*self.popt)
            try:
                if self.Par[1]==4:
                    self.popt, self.perr=fit.V_Fit31L()
                    model=fit.Voigt31L(self.frec,*self.popt)
                else:
                    self.popt, self.perr=fit.V_Fit61L()
                    model=fit.Voigt61L(self.frec,*self.popt)
            except:
                if self.flag==False:
                    messagebox.showerror("Error", 'No se pudo ajustar, modifica los parámetros.')
                    return 0
                else:
                    self.Par[17]=False
                    self.Par[18]='Ajuste'
                #return 0

        else:
            fit=VoigtFit(self.Par,self.frec,self.volt)
            try:
                if self.Par[1]==4:
                    self.popt, self.perr=fit.V_Fit3()
                    model=fit.Voigt3(self.frec,*self.popt)
                else:
                    self.popt, self.perr=fit.V_Fit6()
                    model=fit.Voigt6(self.frec,*self.popt)
            except:
                if self.flag==False:
                    messagebox.showerror("Error", 'No se pudo ajustar, modifica los parámetros.')
                    return 0
                else:
                    self.Par[17]=False
                    self.Par[18]='Ajuste'
                #return 0

        if self.Par[17]==True:
            self.model_Fit=model

            #mask1 = (-100 < self.frec)*(self.frec < 50)
            #self.frec = self.frec[mask1] 
            #self.volt = self.volt[mask1]
            #self.model_Fit = self.model_Fit[mask1]
            #model = model[mask1]

            corr_matrix = corrcoef(self.volt, model)
            corr = corr_matrix[0,1]
            R_1 = corr**2
            r = self.volt - model
            sig=std(r)
            chisq = (sum((r**2) / sig))/(len(self.frec)-len(self.popt))
            self.Par[22]=chisq
            self.Par[23]=R_1

        if self.flag==False:

            if modelType=='Lorentz':
                LS='solid' 
            elif modelType=='Lorentz_1L':
                LS='dotted'
            elif modelType=='Gauss':
                LS='dashed'
            elif modelType=='Voigt':
                LS='dashdot'
            elif modelType=='Voigt_1L':
                LS=(0,(3,1,1,1,1,1))


            self.B_Analizar['state']='normal'
            #self.ax1.plot(self.frec,model,linestyle='dashed',\
            #    label=f'{modelType} fit, Chi2={chisq:3.7f}, R2={R_1:3.7f}',linewidth=3)
            self.ax1.plot(self.frec,model,linestyle=LS,\
                label=f'{modelType} fit, R2={R_1:3.7f}',linewidth=3,markersize=10)
            #self.ax1.plot(self.frec,model+sig)
            #self.ax1.plot(self.frec,model-sig)
            self.ax1.legend(loc='best', shadow=True, fontsize=self.LegSize)
            self.fig.canvas.draw()

    def Borrar(self):
        self.B_Analizar['state']='disable'
        self.B_Analizar['bg']='grey'
        self.popt=None
        self.perr=None
        self.modelType=None
        self.ax1.cla()
        self.ax1.set_title(f'{name(self.files[self.findex]).nam}')
        self.Calibrar(self.files[self.findex])
        self.Set_Ax1()
        self.fig.canvas.draw()


    def Calibrar(self,file): 
        self.Par[17]=True
        self.Par[18]=''
        x=Calibracion(self.Par,file)
        if self.Par[11]==1:
            try:
                x.Cal()
                self.Set_Frec(x.frec,x.Volt)
            except:
                if self.flag==False:
                    messagebox.showerror('Error','Este archivo no se puede calibrar con el método seleccionado.')
                    return 0
                else:
                    self.Par[17]=False
                    self.Par[18]='Calibración'
                #return 0
        elif self.Par[11]==2:
            try:
                x.Cal1()
                self.Set_Frec(x.frec,x.Volt)
            except:
                if self.flag==False:
                    messagebox.showerror('Error','Este archivo no se puede calibrar con el método seleccionado.')
                    return 0
                else:
                    self.Par[17]=False
                    self.Par[18]='Calibración'
                #return 0


        if self.Par[27]==1:
            self.Set_Frec(x.frec,x.Volt) #####  uncoment HERE!
        
        #self.frec=x.frec
        #self.volt=x.Volt
        #################################################################
        #mask1 = (self.Par[25] < self.frec)*(self.frec < self.Par[24])
        #self.frec = self.frec[mask1] 
        #self.volt = self.volt[mask1]

        if self.flagFGauss==False:
            if self.Par[1]!=4:
                try:
                    self.FG=FGauss(self.Par,self.frec,self.volt)
                    self.volt=self.FG.SubDoppler
                except:
                    if self.flag==False:
                        messagebox.showerror('Error','Este archivo no se pudo ajustar el fondo Gaussiano.')
                        return 0
                    else:
                        self.Par[18]='Fondo Gaussiano'
                    #return 0

        if self.flag==False:
            self.graf_ax1()

    def Set_Frec(self,frec,volt):
        if self.Par[27]==1:
            self.Par[25]=min(frec)
            self.Par[24]=max(frec)
        mask1 = (self.Par[25] < frec)*(frec < self.Par[24])
        self.frec = frec[mask1] 
        self.volt = volt[mask1]
        ### MODIFICACIÓN NORMALIZA AMPLITUD #####
        #10/07/2022
        #maximo = max(self.volt)
        #self.volt = self.volt/maximo
        #########################################
        self.VEsp = self.volt


    def graf_ax1(self):
        self.ax1.plot(self.frec,self.volt,'.',label='Experimental')
        self.ax1.legend(fontsize=self.LegSize,loc='best',shadow=True)
        #self.ax1.axhline(y=0, color='black', linestyle='dotted')
        self.ax1.set_title(f'{name(self.files[self.findex]).nam} : {self.Par[26][self.Par[10][1]]}')

    def See_Next(self):
        self.findex=self.findex+1
        if self.findex>=len(self.files):
            self.findex=0
        self.ax1.cla()
        #self.ax1.set_title(f'{name(self.files[self.findex]).nam}')
        self.Calibrar(self.files[self.findex])
        self.Set_Ax1()
        self.fig.canvas.draw()

    def See_Previous(self):
        self.findex=self.findex-1
        if self.findex<=-len(self.files):
            self.findex=0
        self.ax1.cla()
        self.Set_Ax1()
        #self.ax1.set_title(f'{name(self.files[self.findex]).nam}')
        self.Calibrar(self.files[self.findex])
        self.fig.canvas.draw()


    def Back1(self):
        close('all')
        if self.Par[1]==4:
            self.master.switch_frame(WinCal,self.Par)
        else:    
            self.master.switch_frame(WinGauss,self.Par)