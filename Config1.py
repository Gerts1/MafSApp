from numpy import zeros

class Transicion():
        def __init__(self,Par=None):
                self.Par=Par
                self.Ref=0
                self.Trans=[]
                self.len_Trans()
                self.Sel_Tran()

        def len_Trans(self):
                if self.Par[1]==4:
                        for i in range(3):
                                self.Trans.append(0)
                else:
                        for i in range(6):
                                self.Trans.append(0)


        def Sel_Tran(self):

                if self.Par[0]=='A': #isotopo 87
                        
                        if self.Par[1]==0: #5S1/2 F=1->5P3/2 #Revisado
                                self.Name='Rb 87, 5S1/2 F=1->5P3/2'
                                self.HS=['F=0','(0:1)','F=1','(0:2)','(1:2)','F=2']
                                self.Trans[0]=-302.07# atómica F=0
                                self.Trans[1]=-265.96# Crossover (0,1)
                                self.Trans[2]=-229.85# Atómica F=1
                                self.Trans[3]=-187.49# Crossover (0,2)
                                self.Trans[4]=-151.38# Crossover (1,2)
                                self.Trans[5]=-72.91# Atómica F=2
                                self.Ref=[self.Trans[4],4] #ReferenciaOK
                        
                        elif self.Par[1]==1:#5S1/2 F=2->5P3/2 #Revisado
                                self.Name='RB 87, 5S1/2 F=2->5P3/2'
                                self.HS=['F=1','(1:2)','F=2','(1:3)','(2:3)','F=3']
                                self.Trans[0]=-229.85# atómica F=1
                                self.Trans[1]=-151.38# Crossover (1,2)
                                self.Trans[2]=-72.91# Atómica F=2
                                self.Trans[3]=-18.055# Crossover (1,3)
                                self.Trans[4]=60.415# Crossover (2,3)
                                self.Trans[5]=193.74# Atómica F=3
                                self.Ref=[self.Trans[4],4] #Referencia Falta REvisar

                        elif self.Par[1]==2:#5S1/2 F=1->6P3/2 #Revisado
                                self.Name='Rb 87, 5S1/2 F=1->6P3/2'
                                self.HS=['F=0','(0:1)','F=1','(0:2)','(1:2)','F=2']
                                self.Trans[0]=-98.934# atómica F=0
                                self.Trans[1]=-87.06# Crossover (0,1)
                                self.Trans[2]=-75.187# Atómica F=1
                                self.Trans[3]=-61.337# Crossover (0,2)
                                self.Trans[4]=-49.463# Crossover (1,2)
                                self.Trans[5]=-23.74# Atómica F=2
                                self.Ref=[self.Trans[4],4] #ReferenciaOk

                        elif self.Par[1]==3:#5S1/2 F=2->6P3/2 #Revisado
                                self.Name='RB 87, 5S1/2 F=2->6P3/2'
                                self.HS=['F=1','(0:1)','F=2','(0:2)','(1:2)','F=3']
                                self.Trans[0]=-75.187# atómica F=1
                                self.Trans[1]=-49.463# Crossover (1,2)
                                self.Trans[2]=-23.74# Atómica F=2
                                self.Trans[3]=-5.938# Crossover (1,3)
                                self.Trans[4]=19.785# Crossover (2,3)
                                self.Trans[5]=63.31# Atómica F=3
                                self.Ref=[self.Trans[4],4] #Referencia Falta Revisar

                        elif self.Par[1]==4:#5P3/2 F=2->5D5/2
                                self.Name='RB 87, 5P3/2 F=3->5D5/2'
                                self.HS=['F=4','F=3','F=2']
                                self.Trans[0]=-27.65# atómica F=4
                                self.Trans[1]=1.17# atómica F=3
                                self.Trans[2]=24.12# atómica F=2
                                self.Ref=[self.Trans[0],0] #Referencia

                elif self.Par[0]=='B': #isotopo 85
                        
                        if self.Par[1]==0: #5S1/2 F=2->5P3/2 # Revisado
                                self.Name='RB 85, 5S1/2 F=2->5P3/2'
                                self.HS=['F=1','(1:2)','F=2','(1:3)','(2:3)','F=3']
                                self.Trans[0]=-113.208# atómica F=1
                                self.Trans[1]=-98522# Crossover (1,2)
                                self.Trans[2]=-83.8355# Atómica F=2
                                self.Trans[3]=-66.822# Crossover (1,3)
                                self.Trans[4]=-52.135# Crossover (2,3)
                                self.Trans[5]=-20.435# Atómica F=3
                                self.Ref=[self.Trans[4],4] #Referencia Falta
                        
                        elif self.Par[1]==1:#5S1/2 F=3->5P3/2 #Revisado
                                self.Name='RB 85, 5S1/2 F=3->5P3/2'
                                self.HS=['F=2','(2:3)','F=3','(2:4)','(3:4)','F=4']
                                self.Trans[0]=-83.8355# atómica F=2
                                self.Trans[1]=-52.135# Crossover (2,3)
                                self.Trans[2]=-20.435# Atómica F=3
                                self.Trans[3]=8.185# Crossover (2,4)
                                self.Trans[4]=39.885# Crossover (3,4)
                                self.Trans[5]=100.205# Atómica F=4
                                self.Ref=[self.Trans[4],4] #Referencia Falta

                        elif self.Par[1]==2:#5S1/2 F=2->6P3/2 #REvisado
                                self.Name='Rb 85, 5S1/2 F=2->6P3/2'
                                self.HS=['F=1','(1:2)','F=2','(1:3)','(2:3)','F=3']
                                self.Trans[0]=-37.2# atómica F=1
                                self.Trans[1]=-32.3# Crossover (1,2)
                                self.Trans[2]=-27.4# Atómica F=2
                                self.Trans[3]=-21.875# Crossover (1,3)
                                self.Trans[4]=-16.975# Crossover (2,3)
                                self.Trans[5]=-6.55# Atómica F=3
                                self.Ref=[self.Trans[4],4] #Referencia Falta

                        elif self.Par[1]==3:#5S1/2 F=3->6P3/2 #Revisado
                                self.Name='Rb 85, 5S1/2 F=3->6P3/2'
                                self.HS=['F=2','(2:3)','F=3','(2:4)','(3:4)','F=4']
                                self.Trans[0]=-27.4# atómica F=2
                                self.Trans[1]=-16.975# Crossover (2,3)
                                self.Trans[2]=-6.55# Atómica F=3
                                self.Trans[3]=2.66# Crossover (2,4)
                                self.Trans[4]=13.084# Crossover (3,4)
                                self.Trans[5]=32.719# Atómica F=4
                                self.Ref=[self.Trans[4],4] #Referencia Falta

                        elif self.Par[1]==4:#5P3/2 F=2->5D5/2
                                # Falta Calcular!!
                                self.Name='RB 85, 5P3/2 F=4->5D5/2'
                                self.HS=['F=4','F=3','F=2']
                                self.Trans[0]=-27.65# atómica F=4
                                self.Trans[1]=1.17# atómica F=3
                                self.Trans[2]=24.12# atómica F=2
                                self.Ref=[self.Trans[0],0] #Referencia