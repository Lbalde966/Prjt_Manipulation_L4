# Prjt_Manipulation_L4
manipulation bras robot

Cette application est une interface graphique (développée avec Tkinter) conçue pour superviser et contrôler un robot et ses équipements périphériques. Le programme permet de communiquer avec le robot via un port série, de visualiser et piloter une caméra IP (mouvements et enregistrement vidéo), et de gérer un lecteur de badges RFID avec enregistrement des données dans une base de données MySQL.

main.py : Fichier d'exécution principal qui initialise la fenêtre principale, connecte le contrôleur vidéo à l'adresse IP de la caméra, ajoute l'interface de commande textuelle, et lance l'application.

IHM_ROBOT.py : Définit la fenêtre principale de l'application et assemble les différentes interfaces graphiques (caméra et RFID) au sein de cette même fenêtre.

IHM_MA_COMMANDE.py : Interface graphique "Terminal Robot" qui inclut des boutons pour scanner et se connecter aux ports COM. Elle offre une console textuelle pour envoyer des commandes au robot et lire ses réponses.

Connexion_serie.py : Thread fonctionnant en arrière-plan pour gérer la communication série. Il lit en continu les données entrantes pour les afficher dans la zone de texte et possède une méthode pour envoyer des commandes avec les bons retours à la ligne.

Serie_controle.py : Classe utilitaire qui détecte et retourne la liste de tous les ports COM (série) disponibles sur l'ordinateur.

IHM_CAMERA.py : Interface graphique affichant le flux de la caméra IP. Elle contient des boutons et des raccourcis clavier pour diriger la caméra (haut, bas, gauche, droite), lancer l'affichage vidéo ou déclencher un enregistrement. Elle envoie les requêtes de mouvement via des adresses HTTP.

Video_controle.py : Fait le pont entre l'interface graphique et le flux vidéo. Il lance ou arrête le thread de capture, redimensionne les images pour l'affichage, et gère l'enregistrement du flux dans un fichier .avi situé dans les téléchargements.

Video_thread.py : Thread lisant le flux vidéo de l'adresse IP en continu grâce à la bibliothèque OpenCV et envoyant les images au contrôleur.

IHM_RFID.py : Interface graphique dédiée au lecteur de badges. Elle permet de sélectionner le port série du lecteur et affiche l'UID du dernier tag lu.

Rfid_thread.py : Thread écoutant en permanence le lecteur RFID sur le port série. Il isole l'identifiant du badge lu, prévient l'interface graphique pour l'affichage, et enregistre automatiquement cet identifiant dans une base de données MySQL locale.
