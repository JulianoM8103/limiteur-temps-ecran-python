# Import des modules
import json
from tkinter import *
from tkinter.messagebox import *

log = open("logs/setup.txt", 'w+') # Ouvre le fichier de logs
log.write("[*] Le fichier de logs est pret a etre ecrit !") # Log

class Index(Tk):
    def __init__(self):

        Tk.__init__(self)
        self.title("Options du controle parental") # Titre de la fenêtre
        self.geometry("285x200") # Taille de la fenêtre
        self.resizable(width=False, height=False) # Empeche le redimensionnement de la fenetre
        self.window()

    def window(self):

        with open("infos.json") as infos:
            self.data = json.load(infos)
            self.max_duration = self.data['infos']['max_duration'] # Récupère la durée maximale de temps d'écran en seconde
            self.max_dur = int(self.max_duration) / 60 / 60 # Convertit le temps maximal d'écran en heures

        self.info = Label(self, text=f"Durée maximale actuelle : {self.max_dur}h \n") # Affiche la durée maximale d'heures d'écran autorisés inscrite dans le fichier
        self.info.pack() 

        self.duration = Label(self, text="Nouvelle durée maximale d'écran (en heures)")
        self.duration.pack()

        self.max_duration_entry = Entry(self) # Zone de texte pour entrer le nouveau temps d'écran maximal
        self.max_duration_entry.pack()

        self.add_task_button = Button(self, text="Mettre à jour", command=lambda: self.set_max_duration(self.max_duration_entry.get())) # Boutton pour mettre à jour les données dans infos.json
        self.add_task_button.pack()

        self.ask = Label(self, text="\nVoulez vous réintialiser le compteur d'aujourd'hui ?") # Info
        self.ask.pack()

        self.reset_button = Button(self, text="Réintialiser", command=lambda: self.reintialisation()) # Button pour réintialiser le compteur du jour
        self.reset_button.pack()

        log.write("\n[*] Lancement de l'application de setup") # Log

        self.mainloop() # Ouvre la fenêtre

    def set_max_duration(self, max_duration):

        try:
            max_dur = int(max_duration) * 60 * 60 # Convertit le temps d'écran maximal en heures (initialement en secondes)

        except(ValueError):

            if max_duration == '':
                log.write(f"\n[!] ValueError : Aucun nombre n'a ete rentrer") # Log
                showerror(title="Erreur", message="Vous devez rentrer un nombre !") # Fenêtre d'erreur
            else:
                log.write(f"\n[!] ValueError : Un nombre a virgule a ete rentrer") # Log
                showerror(title="Erreur", message="Vous ne pouvez pas utiliser des nombres à virgule !") # Fenêtre d'erreur

        except(UnboundLocalError):
            log.write(f"\n[!] Impossible d'acceder a la variable 'max_dur' car elle n'est pas associee a une valeur") # Log

        self.data['infos']['max_duration'] = max_dur # Enregistre le nouveau temps d'écran maximal

        with open("infos.json", "w") as f:
            json.dump(self.data, f, indent=4) # Ecrit le nouveau temps dans le fichier infos.json
            log.write("\n[*] Nouveau temps d'ecran maximal defini !") # Log

    def reintialisation(self):

        with open("infos.json", "r") as f:
            self.data = json.load(f) # Lis le fichier infos.json

        self.newDuration = self.data["infos"]["max_duration"] # Enregistre la nouvelle valeur de 'duration'
        self.data['infos']['duration'] = self.newDuration # Idem

        with open("infos.json", "w") as f:
            json.dump(self.data, f, indent=4) # Ecrit dans le fichier infos.json la nouvelle valeur de 'duration'
            log.write("\n[*] Compteur du jour reintialiser") # Log
        
window = Index()