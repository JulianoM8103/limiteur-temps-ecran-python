# Import des modules
import os
import json
from tkinter import *
from tkinter.messagebox import *

log = open("logs/main.txt", 'w+') # Ouvre le fichier de logs
log.write("[*] Le fichier de logs est pret a etre ecrit !") # Log

class Index(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Temps d'écran")
        self.geometry("500x200")
        self.resizable(width=False, height=False) # Empeche le redimensionnement de la fenetre
        self.window()

    def window(self):
        with open("infos.json") as infos:
            self.data = json.load(infos) # Lis le fichier infos.json
            self.max_duration = self.data['infos']['max_duration'] # Récupère la durée maximale autorisée
            self.max_durationH = int(self.max_duration) / 60 / 60 # La convertit en heures
            self.duration = self.data['infos']['duration'] # Compteur

            if self.duration == 0:
                log.write("\n[!] Limite de temps d'ecran atteinte. L'ordinateur va s'etteindre") # Log
                os.system('shutdown -s') # Eteint l'ordinateur dans la minute qui suit
                self.destroy() # Ferme la fenêtre

        self.info = Label(self, text=f"Temps d'écran restant : {self.duration}sec", font=("Helvetica", 16)) # Compteur
        self.info.pack()

        self.max = Label(self, text=f"\nTemps d'écran maximal : {self.max_duration}sec soit {self.max_durationH}h", font=("Helvetica", 16))
        self.max.pack()

        self.update_label() # Lance le compteur

        log.write("\n[*] Ouverture de la fenetre du compteur") # Log
        self.mainloop() # Ouvre la fenêtre

        self.protocol("WM_DELETE_WINDOW", self.fermeture()) # Détecte quand la fenêtre est fermée

    def update_label(self):
        with open("infos.json", 'r') as infos:
            self.data = json.load(infos) # Lis le fichier infos.json
            self.max_duration = self.data['infos']['max_duration'] # Récupère la durée maximale autorisée
            self.max_durationH = int(self.max_duration) / 60 / 60 # La convertit en heures
            self.duration -= 1 # Compteur

        if int(self.duration) == 0: # Si le compteur est à O
            os.system('shutdown -s') # Eteint l'ordinateur dans la minute qui suit
            self.destroy() # Ferme la fenêtre

        self.info.config(text=self.duration)

        with open("infos.json", "w") as f:
            self.data['infos']['duration'] = self.duration # Récupère et enregistre la nouvelle valeur du compteur
            json.dump(self.data, f, indent=4) # L'écrit dans le fichier infos.json

        self.after(1000, self.update_label) # Attend 1 seconde avant de recommencer

    def fermeture(self):
        log.write("\n[!] La fenetre est fermee, reouverture") # Log
        Index() # Relance le programme quand la fenêtre est fermée

window = Index()
