import tkinter as tk
from data import *
from .courses_choice_page import CoursesChoicePage
from dataTools import *
from pages.teacher_page import TeacherPage

class MasterChoicePage(tk.Frame):
    """
    Page permettant de choisir un master après le scan d'une carte d'enseignant.

    Attributs
    ----------
    parent : tk.Widget
        Le widget parent de cette page.
    controller : App
        L'instance de contrôleur de l'application.

    Méthodes
    --------
    select_master(master, controller)
        Sélectionne un master et navigue vers la page de choix de cours.
    """
    def __init__(self, parent, controller):
        """
        Initialise la page de choix de master avec un label et un bouton pour chaque master.

        Paramètres
        ----------
        parent : tk.Widget
            Le widget parent de cette page.
        controller : App
            L'instance de contrôleur de l'application.
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choisissez un master")
        label.pack(side="top", fill="x", pady=10)

        db_conn = create_connection()

        # Get the names of the masters
        masters = get_master_name(db_conn)
        
        # Create a button for each master
        for master in masters:
            button = tk.Button(self, text=master,
                               command=lambda master=master: self.select_master(master, controller))
            button.pack()
            
        # Create back button
        back_button = tk.Button(self, text="Retour",
                                command=lambda: controller.show_frame(TeacherPage))
        back_button.pack(side="left", anchor="sw")
        
    def select_master(self, master, controller):
        """
        Sélectionne un master et navigue vers la page de choix de cours.

        Paramètres
        ----------
        master : str
            Le nom du master sélectionné.
        controller : App
            L'instance de contrôleur de l'application.
        """
        controller.selected_master = master
        print(f"Selected master: {master}")
        controller.show_frame(CoursesChoicePage)
