from IHM_ROBOT import IHM_ROBOT
from Video_controle import Video_controle
from IHM_MA_COMMANDE import IHM_MA_COMMANDE

#main 
URL = "http://172.20.81.168:8000/videostream.cgi?user=admin&pwd=0000"
ihm=IHM_ROBOT()
control_video=Video_controle(ihm.IHM_CAMERA,URL)

ma_commande_robot = IHM_MA_COMMANDE(ihm.fenetre)
ma_commande_robot.grid(row=1, column=1, padx=15, pady=20) # Le "n" empêche l'étirement vers le bas

ihm.start()