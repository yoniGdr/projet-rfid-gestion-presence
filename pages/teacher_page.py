import tkinter as tk
from mfrc522 import SimpleMFRC522
from dataTools import is_teacher_id_valid

from data import create_connection

reader = SimpleMFRC522()

class TeacherPage(tk.Frame):
    """
    Page d'accueil de l'application. Attend le scan d'une carte d'enseignant.

    Attributs
    ----------
    parent : tk.Widget
        Le widget parent de cette page.
    controller : App
        L'instance de contrôleur de l'application.
    label : tk.Label
        Le label indiquant l'état actuel ("En attente du scan d'un professeur").
    db_conn : sqlite3.Connection
        La connexion à la base de données.

    Méthodes
    --------
    scan_teacher_card()
        Commence à scanner pour une carte d'enseignant.
    start_scanning()
        Redémarre le scanner.
    """
    def __init__(self, parent, controller):
        """
        Initialise la page d'accueil avec un label.

        Paramètres
        ----------
        parent : tk.Widget
            Le widget parent de cette page.
        controller : App
            L'instance de contrôleur de l'application.
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="En attente du scan d'un professeur")
        self.label.place(relx=0.5, rely=0.5, anchor="center")  # Place le widget au centre de la fenêtre

        self.db_conn = create_connection()
        self.scan_teacher_card()

    def scan_teacher_card(self):
        """
        Commence à scanner pour une carte d'enseignant. Si une carte est détectée et est valide, 
        navigue vers la page de choix du master. Sinon, continue à scanner.
        """
        from .master_choice_page import MasterChoicePage
        
        if self.controller.current_page == 'StudentPage':
            return
        if self.controller.current_page == 'MasterChoicePage':
            return
        id, text = reader.read_no_block()
        if is_teacher_id_valid(self.db_conn, str(id)):
        
            self.controller.show_frame(MasterChoicePage)
        else:
            self.after(1000, self.scan_teacher_card)
            
    def start_scanning(self):
        """
        Redémarre le scanner. C'est nécessaire car le scanner s'arrête de scanner lorsqu'il détecte une carte.
        Cette méthode est appelée chaque fois que cette page est affichée à l'écran.
        """
        self.scan_teacher_card()
