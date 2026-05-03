import tkinter
import requests
import time
# from Video_thread import Video_thread


class IHM_CAMERA(tkinter.LabelFrame):
    def __init__(self, parent,
                 on_start=None,
                 on_stop=None,
                 on_record_start=None,
                 on_record_stop=None):
        super().__init__(parent)

        self.etat = False
        self.recording = False

        self.on_start = on_start
        self.on_stop = on_stop
        self.on_record_start = on_record_start
        self.on_record_stop = on_record_stop

        # Paramètres caméra
        self.ip_camera = "172.20.81.168:8000"
        self.user = "admin"
        self.pwd = "0000"

        # Délai entre commandes PTZ
        self.delai = 0.2

        self["text"] = "commande camera"
        self["labelanchor"] = "nw"

        self.texte = tkinter.Label(self, text="c'est ici que l'on gère la caméra")
        self.texte.grid(row=1, column=2, columnspan=3)

        self.canvas_camera = tkinter.Canvas(self, width=640, height=480, bg='ivory')
        self.canvas_camera.grid(row=2, column=1, columnspan=5)

        # Bouton vidéo
        self.bouton = tkinter.Button(self, text='video', command=self.video)
        self.bouton.grid(row=3, column=2, columnspan=3, pady=5)

        # Bouton enregistrement
        self.bouton_rec = tkinter.Button(self, text='REC OFF', bg='lightgray', command=self.record)
        self.bouton_rec.grid(row=4, column=2, columnspan=3, pady=5)

        # Boutons directionnels
        self.bouton_haut = tkinter.Button(self, text="↑", width=6, command=self.camera_haut)
        self.bouton_bas = tkinter.Button(self, text="↓", width=6, command=self.camera_bas)
        self.bouton_gauche = tkinter.Button(self, text="←", width=6, command=self.camera_gauche)
        self.bouton_droite = tkinter.Button(self, text="→", width=6, command=self.camera_droite)
        self.bouton_stop = tkinter.Button(self, text="STOP", width=8, command=self.camera_stop)

        self.bouton_haut.grid(row=5, column=3, pady=2)
        self.bouton_gauche.grid(row=6, column=2, sticky="e")
        self.bouton_stop.grid(row=6, column=3)
        self.bouton_droite.grid(row=6, column=4, sticky="w")
        self.bouton_bas.grid(row=7, column=3, pady=2)

        # Contrôles clavier
        self.bind_all("<Up>", self.clavier_haut)
        self.bind_all("<Down>", self.clavier_bas)
        self.bind_all("<Left>", self.clavier_gauche)
        self.bind_all("<Right>", self.clavier_droite)
        self.bind_all("<space>", self.clavier_stop)

        # Touche R pour l'enregistrement
        self.bind_all("<r>", self.clavier_record)
        self.bind_all("<R>", self.clavier_record)

    # ==========================
    # Gestion vidéo
    # ==========================

    def video(self):
        print("bouton video", self.etat)
        if self.etat:
            self.etat = False
            if self.on_stop is not None:
                self.on_stop()
        else:
            self.etat = True
            if self.on_start is not None:
                self.on_start()

    def record(self):
        print("bouton enregistrement", self.recording)

        if self.recording:
            self.recording = False
            self.bouton_rec.config(text="REC OFF", bg="lightgray")
            print("Enregistrement arrêté")
            if self.on_record_stop is not None:
                self.on_record_stop()
        else:
            self.recording = True
            self.bouton_rec.config(text="REC ON", bg="red")
            print("Enregistrement démarré")
            if self.on_record_start is not None:
                self.on_record_start()

    def afficher(self, photo):
        self.photo = photo
        self.canvas_camera.create_image(0, 0, anchor="nw", image=self.photo)

    def effacer(self):
        self.canvas_camera.delete("all")

    # ==========================
    # Setters callbacks
    # ==========================

    def set_on_start(self, on_start):
        self.on_start = on_start
        print("set on-start")

    def set_on_stop(self, on_stop):
        self.on_stop = on_stop
        print("set on-stop")

    def set_on_record_start(self, on_record_start):
        self.on_record_start = on_record_start
        print("set on-record-start")

    def set_on_record_stop(self, on_record_stop):
        self.on_record_stop = on_record_stop
        print("set on-record-stop")

    # ==========================
    # Commandes caméra PTZ
    # ==========================

    def envoyer_commande_camera(self, command):
        url = f"http://{self.ip_camera}/decoder_control.cgi?command={command}&user={self.user}&pwd={self.pwd}"
        print("Envoi commande :", url)

        try:
            requests.get(url, timeout=2)
            time.sleep(self.delai)
        except Exception as e:
            print("Erreur commande caméra :", e)

    def camera_haut(self):
        print("Commande : haut")
        self.envoyer_commande_camera(0)

    def camera_bas(self):
        print("Commande : bas")
        self.envoyer_commande_camera(2)

    def camera_gauche(self):
        print("Commande : gauche")
        self.envoyer_commande_camera(4)

    def camera_droite(self):
        print("Commande : droite")
        self.envoyer_commande_camera(6)

    def camera_stop(self):
        print("Commande : stop")
        self.envoyer_commande_camera(1)

    # ==========================
    # Contrôle clavier direction
    # ==========================

    def clavier_haut(self, event):
        print("Flèche haut")
        self.camera_haut()

    def clavier_bas(self, event):
        print("Flèche bas")
        self.camera_bas()

    def clavier_gauche(self, event):
        print("Flèche gauche")
        self.camera_gauche()

    def clavier_droite(self, event):
        print("Flèche droite")
        self.camera_droite()

    def clavier_stop(self, event):
        print("Espace → STOP")
        self.camera_stop()

    # ==========================
    # Contrôle clavier enregistrement
    # ==========================

    def clavier_record(self, event):
        print("Touche R → enregistrement")
        self.record()