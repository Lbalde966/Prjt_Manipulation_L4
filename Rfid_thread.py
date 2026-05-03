import threading
import serial
import mysql.connector

class Rfid_thread(threading.Thread):
    def __init__(self, port, callback_affichage):
        super().__init__(daemon=True)
        self.port = port
        self.callback_affichage = callback_affichage
        self.running = True
        
        # Connexion BDD
        self.db = mysql.connector.connect(
            host="localhost", user="robotroi", password="robotroi", database="Microbe"
        )
        self.cursor = self.db.cursor()
        self.ser = serial.Serial(self.port, 9600, timeout=1)

    def run(self):
        dernier_uid = ""
        while self.running:
            byte = self.ser.read(1)
            if byte:
                length_byte = self.ser.read(1)
                if length_byte:
                    length = ord(length_byte)
                    payload = self.ser.read(length - 2)
                    if len(payload) >= 6:
                        uid_bytes = payload[1:7]
                        uid_actuel = "".join(f"{b:02X}" for b in uid_bytes)

                        if uid_actuel != dernier_uid:
                            # Insertion BDD
                            self.cursor.execute("INSERT INTO badges (uid) VALUES (%s)", (uid_actuel,))
                            self.db.commit()
                            
                            # Envoi à l'IHM via le callback
                            self.callback_affichage(uid_actuel)
                            dernier_uid = uid_actuel
                            
    def stop(self):
        self.running = False
        self.ser.close()