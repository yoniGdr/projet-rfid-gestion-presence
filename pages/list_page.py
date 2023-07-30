import tkinter as tk
from tkinter import messagebox
from mfrc522 import SimpleMFRC522
from data import *
from dataTools import *

class ListPage(tk.Frame):
    """
    Page affichant la liste des étudiants présents à un cours donné.

    Attributs
    ----------
    parent : tk.Widget
        Le widget parent de cette page.
    controller : App
        L'instance de contrôleur de l'application.

    Méthodes
    --------
    refresh()
        Met à jour la liste des étudiants présents à l'écran.
    """
    def __init__(self, parent, controller):
        """
        Initialise la page de liste avec un label de titre, un nouveau cadre pour les noms d'étudiants,
        et un bouton pour revenir à la page de scan.

        Paramètres
        ----------
        parent : tk.Widget
            Le widget parent de cette page.
        controller : App
            L'instance de contrôleur de l'application.
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Liste des étudiants présents", font=("Helvetica", 10, "bold", "underline"))
        self.label.pack(side="top", fill="x", pady=10)
        
        self.students_frame = tk.Frame(self)  # nouveau Frame pour contenir les labels des étudiants
        self.students_frame.place(relx=0.5, rely=0.2, anchor='center')  # centre le Frame
        
        # bouton pour retourner à la page précédente
        from .student_page import StudentPage
        back_button = tk.Button(self, text="Retour",
                               command=lambda: controller.show_frame(StudentPage))
        back_button.pack(side="left", anchor="sw") 
        

    def refresh(self):
        """
        Met à jour la liste des étudiants présents à l'écran.

        Cette fonction efface tous les labels d'étudiants actuels, récupère la liste des étudiants
        présents pour le cours sélectionné, et crée un nouveau label pour chaque étudiant présent.
        """
        # supprime toutes les anciennes entrées de la liste
        for widget in self.students_frame.winfo_children():
            widget.destroy()

        # récupére la liste des étudiants présents au cours actuel
        students = get_present_students(self.controller.selected_course)
        # affiche chaque étudiant dans la liste
        for student in students:
            student_label = tk.Label(self.students_frame, text=student)
            student_label.pack()
