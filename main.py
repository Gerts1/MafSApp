from tkinter import Tk
from tkinter.font import Font
from GUIcode import Win1
from matplotlib.font_manager import FontProperties


class MafSApp(Tk):
    def __init__(self):
        super().__init__()
        self.wm_title('MafSApp')
        self._frame = None
        self.Par=['A',0,0,'s',0,0,0,0,1,1,2,9,12,13,14,15,16,True,'',False,False,False,False,False,0,0,0,0]
        self.fontT = Font(family="Helvetica",size=18,weight="bold")
        self.fontl = Font(family="Helvetica",size=10,weight="bold")
        self.fontAxis = FontProperties(size=12,weight="medium")
        self.LegSize = 12
        self.switch_frame(Win1,self.Par)

    def switch_frame(self, frame_class,Par):
        new_frame = frame_class(self,Par)
        if self._frame is not None:           
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    
app = MafSApp()
app.mainloop()
del app