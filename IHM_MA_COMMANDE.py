# -*- coding: utf-8 -*-
import tkinter 
from Serie_controle import Serie_controle
from Connexion_serie import Connexion_serie

class IHM_MA_COMMANDE(tkinter.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self["text"] = "Terminal Robot"
        self["labelanchor"] = 'nw'
        self.configure(bg="black", fg="white")

        # ==========================================
        # BARRE DE CONNEXION (Alignée comme sur ton screenshot)
        # ==========================================
        cadre_haut = tkinter.Frame(self, bg="black")
        cadre_haut.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # 1. Bouton Scan
        self.bouton_scanner = tkinter.Button(cadre_haut, text="Scan", command=self.scanner_ports)
        self.bouton_scanner.pack(side='left', padx=5)
        
        # 2. Menu déroulant
        self.lst1 = ['COM1'] # Valeur par défaut
        self.var1 = tkinter.StringVar()
        self.var1.set(self.lst1[0])
        self.drop = tkinter.OptionMenu(cadre_haut, self.var1, *self.lst1)
        self.drop.pack(side='left', padx=5)
        
        # 3. Bouton Connexion
        self.bouton_connexion = tkinter.Button(cadre_haut, text="Connexion", command=self.connexion_port)
        self.bouton_connexion.pack(side='left', padx=5)

        # ==========================================
        # ZONE DE TEXTE CLASSIQUE
        # ==========================================
        self.text_console = tkinter.Text(self, width=60, height=15, bg="black", fg="#00FF00", font=("Consolas", 10))
        self.text_console.grid(row=3, column=1, padx=5, pady=5)
        
        # ==========================================
        # BARRE D'ENTRÉE POUR TAPER LES COMMANDES
        # ==========================================
        self.entree_commande = tkinter.Entry(self, bg="#222222", fg="white", insertbackground="white")
        self.entree_commande.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        self.entree_commande.bind('<Return>', self.envoyer)
        
        self.connexion = None

    # --- FONCTION 1 : LE SCAN ---
    def scanner_ports(self):
        print("Recherche des ports en cours...")
        serie_controle = Serie_controle()       
        ports_trouves = serie_controle.scanner_ports()
        
        if ports_trouves:
            self.lst1 = ports_trouves
            menu = self.drop["menu"]
            menu.delete(0, 'end') # On vide l'ancienne liste
            for p in self.lst1:
                menu.add_command(label=p, command=tkinter._setit(self.var1, p)) # On ajoute les nouveaux
            
            # On affiche le dernier port trouvé (souvent c'est le robot !)
            self.var1.set(self.lst1[-1]) 
            print(f"Ports trouvés : {self.lst1}")

    # --- FONCTION 2 : LA CONNEXION ---
    def connexion_port(self):
        port_choisi = self.var1.get()
        
        # Sécurité : vérifier qu'on ne se connecte pas 2 fois
        if self.connexion is not None:
            self.text_console.insert(tkinter.END, "⚠️ Vous êtes déjà connecté !\n")
            return
            
        print(f"Tentative de connexion au port: {port_choisi}")
        self.text_console.insert(tkinter.END, f"Connexion à {port_choisi}...\n")
        
        # Lancement de la connexion
        self.connexion = Connexion_serie(port_choisi, self.text_console)
        self.connexion.start()

    # --- FONCTION 3 : L'ENVOI DE TEXTE ---
    def envoyer(self, event=None):
        commande = self.entree_commande.get()
        if self.connexion:
            self.connexion.envoyer_commande(commande)
            self.text_console.insert(tkinter.END, f"Toi > {commande}\n")
            self.text_console.see(tkinter.END)
        else:
            self.text_console.insert(tkinter.END, "⚠️ Connectez-vous d'abord !\n")
        
        self.entree_commande.delete(0, tkinter.END)