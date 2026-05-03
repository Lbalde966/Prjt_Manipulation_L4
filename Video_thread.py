# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:43:47 2026

@author: ebrembilla
"""
import cv2
import threading

class Video_thread(threading.Thread):
    def __init__(self,url,callback):
        super().__init__(daemon=True)
        self.url=url
        self.callback = callback # fonction du controller appelée à chaque frame
        self.running = False
        self.cap = None
        
    def run(self):
        self.cap = cv2.VideoCapture(self.url)
        if not self.cap.isOpened():
            print("Impossible de se connecter à la caméra")
            return
        self.running = True
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            self.callback(frame) # envoie la frame brute BGR au controller
        self.cap.release()
            
    def stop(self):
        self.running = False

