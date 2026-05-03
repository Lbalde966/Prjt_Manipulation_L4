# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 15:41:32 2026

@author: ebrembilla
"""

from threading import Thread
import serial

class Connexion_serie(Thread):
    def __init__(self,port,zone_text):
        super().__init__()
        self.port=port
        self.zone_text=zone_text
        
        self.stop=False
        
        self.ser=serial.Serial(self.port,baudrate=9600,timeout=1)
        
        
    def run(self):
        
        while not self.stop:
            data=self.ser.readline().decode('utf-8').strip()
            if data:
                self.zone_text.insert('insert',data)
                
    def stop_connexion(self):
        self.stop=True
        
    def envoyer_commande(self,commande):
        mot=(commande+'\n\r\n').encode('utf-8')
        self.ser.write(mot)
        
        