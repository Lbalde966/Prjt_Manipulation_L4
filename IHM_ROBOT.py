# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:41:38 2026

@author: ebrembilla
"""

import tkinter
#from IHM_COMMANDE_ROBOT import IHM_COMMANDE_ROBOT
from IHM_CAMERA import IHM_CAMERA
from IHM_RFID import IHM_RFID


class IHM_ROBOT():
    def __init__(self):
        self.fenetre=tkinter.Tk()
        
        #self.IHM_COMMANDE_ROBOT=IHM_COMMANDE_ROBOT(self.fenetre)
        #self.IHM_COMMANDE_ROBOT.grid(row=1,column=1,rowspan=2)
        
        self.IHM_CAMERA=IHM_CAMERA(self.fenetre)
        self.IHM_CAMERA.grid(row=1,column=2)
        
        self.IHM_RFID=IHM_RFID(self.fenetre)
        self.IHM_RFID.grid(row=2,column=1)
        

        
    def start(self):
        self.fenetre.mainloop()
        