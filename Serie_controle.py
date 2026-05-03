# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 13:40:14 2026

@author: ebrembilla
"""

import serial
import serial.tools.list_ports

class Serie_controle():
    def __init__(self):
        self.liste_com=[]
        
        
    def scanner_ports(self):
        ports=serial.tools.list_ports.comports()
        
        if not ports:
            print("Aucun port série détecté")
            return
        for port in sorted(ports):
            print(port.name)
            self.liste_com.append(port.device)
        return self.liste_com
        
        