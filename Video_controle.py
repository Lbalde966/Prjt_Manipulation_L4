# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 16:13:44 2026

@author: ebrembilla
"""

import cv2
import os
from PIL import Image, ImageTk
from Video_thread import Video_thread
# from IHM_CAMERA import IHM_CAMERA


class Video_controle:
    def __init__(self, ihm_camera=None, url=None):
        self.ihm_camera = None
        self.url = url
        self.capture = None

        # Etat enregistrement
        self.recording = False
        self.video_writer = None

        # Nom du fichier vidéo
        self.chemin_video = os.path.join(os.path.expanduser("~"), "Downloads", "video_camera.avi")

        self.set_ihm_camera(ihm_camera)

    def demarrer(self):
        print("controle demarrer")
        self.capture = Video_thread(self.url, callback=self.on_frame)
        self.capture.start()

    def arreter(self):
        print("controle arreter")
        if self.capture:
            self.capture.stop()
            self.capture = None

        # Si un enregistrement est en cours, on l'arrête aussi
        if self.recording:
            self.stop_record()

        self.ihm_camera.effacer()

    def start_record(self):
        print("Démarrage enregistrement")

        # Evite de relancer si déjà actif
        if self.recording:
            print("Enregistrement déjà actif")
            return

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.video_writer = cv2.VideoWriter(self.chemin_video, fourcc, 20.0, (640, 480))

        if not self.video_writer.isOpened():
            print("Erreur : impossible de créer le fichier vidéo")
            self.video_writer = None
            return

        self.recording = True
        print("Enregistrement démarré")
        print("Fichier :", self.chemin_video)

    def stop_record(self):
        print("Arrêt enregistrement")

        self.recording = False

        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

        print("Enregistrement arrêté")
        print("Vidéo sauvegardée dans :", self.chemin_video)

    def on_frame(self, frame):
        print("controle on_frame")
        """
        Appelé par le thread Model - conversion BGR -> ImageTk puis envoi à la View.
        """

        # Enregistrement vidéo si activé
        if self.recording and self.video_writer is not None:
            frame_resize = cv2.resize(frame, (640, 480))
            self.video_writer.write(frame_resize)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2.resize(frame_rgb, (640, 480)))
        photo = ImageTk.PhotoImage(image=img)

        # Repasse dans le thread principal pour toucher à Tkinter
        self.ihm_camera.after(0, self.ihm_camera.afficher, photo)

    def set_ihm_camera(self, ihm_camera):
        print("control set on-stat, on-stop")
        self.ihm_camera = ihm_camera

        if self.ihm_camera is not None:
            self.ihm_camera.set_on_start(self.demarrer)
            self.ihm_camera.set_on_stop(self.arreter)

            # Ajout callbacks enregistrement
            self.ihm_camera.set_on_record_start(self.start_record)
            self.ihm_camera.set_on_record_stop(self.stop_record)