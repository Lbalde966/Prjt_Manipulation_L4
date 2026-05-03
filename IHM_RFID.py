import tkinter
from Serie_controle import Serie_controle
from Rfid_thread import Rfid_thread

class IHM_RFID(tkinter.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.lst1 = []
        self.rfid_thread = None 

        self["text"] = "info RFID et tapis"
        self["labelanchor"] = 'nw'
        
        # --- Affichage du Tag ---
        self.texte = tkinter.Label(self, text="En attente de badge...", fg="blue", font=("Arial", 10, "bold"))
        self.texte.grid(row=0, column=1, columnspan=2, pady=5)
        
        # --- Contrôles Port Com ---
        self.bouton_scanner_port_com = tkinter.Button(self, text="scan port com", command=self.scanner_ports)
        self.bouton_scanner_port_com.grid(row=1, column=1)
        
        self.lst1 = ['scanner ports']
        self.var1 = tkinter.StringVar()
        self.var1.set(self.lst1[0])
        self.drop = tkinter.OptionMenu(self, self.var1, *self.lst1) 
        self.drop.grid(row=2, column=1)
        
        self.bouton_connexion_port_com = tkinter.Button(self, text="connexion port com", command=self.connexion_port)
        self.bouton_connexion_port_com.grid(row=2, column=2)
        
    def connexion_port(self):
        port_choisi = self.var1.get()
        print("Connexion au port:", port_choisi)
        
        # On lance le thread si ce n'est pas déjà fait
        if self.rfid_thread is None or not self.rfid_thread.is_alive():
            self.rfid_thread = Rfid_thread(port_choisi, self.maj_affichage_uid)
            self.rfid_thread.start()
            self.texte.config(text="Lecteur actif", fg="green")
        
    def maj_affichage_uid(self, uid):
        # Cette fonction est appelée par le Thread dès qu'un badge est lu
        self.texte.config(text=f"Tag lu : {uid}", fg="red")

    def scanner_ports(self):
        serie_controle = Serie_controle()       
        self.lst1 = serie_controle.scanner_ports()
        
        menu = self.drop['menu']
        menu.delete(0, 'end')
        if self.lst1:
            for p in self.lst1:
                menu.add_command(label=p, command=tkinter._setit(self.var1, p))
            self.var1.set(self.lst1[0])