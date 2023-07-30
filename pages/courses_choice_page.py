import tkinter as tk
import datetime
from data import *
from dataTools import *
from .student_page import StudentPage
from pages.teacher_page import TeacherPage

class CoursesChoicePage(tk.Frame):
    """
    Page permettant de choisir un cours après la sélection d'un master.

    Attributs
    ----------
    parent : tk.Widget
        Le widget parent de cette page.
    controller : App
        L'instance de contrôleur de l'application.

    Méthodes
    --------
    refresh()
        Met à jour la liste des boutons de cours en fonction du master sélectionné.
    select_course(controller, course)
        Sélectionne un cours, le stocke dans le contrôleur et navigue vers la page d'attente des étudiants.
    """
    def __init__(self, parent, controller):
        """
        Initialise la page de choix de cours avec un label, un cadre pour les boutons de cours, 
        et un bouton de retour.

        Paramètres
        ----------
        parent : tk.Widget
            Le widget parent de cette page.
        controller : App
            L'instance de contrôleur de l'application.
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Choisissez un cours")
        self.label.pack(side="top", fill="x", pady=10)
        self.buttons_frame = tk.Frame(self)  # Nouveau cadre pour contenir les boutons
        self.buttons_frame.pack()
        
        # Connect to the database
        self.db_conn = create_connection()
        
        # Create back button
        back_button = tk.Button(self, text="Retour",
                                command=lambda: controller.show_frame(TeacherPage))
        back_button.pack(side="left", anchor="sw")  # Pack it at the bottom left corner

    def refresh(self):
        """
        Met à jour la liste des boutons de cours en fonction du master sélectionné.
        Supprime les anciens boutons de cours et en crée de nouveaux.
        """
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        master_name = self.controller.selected_master
        print(master_name)
        courses = get_course_list_by_master(master_name)
        # Create a button for each course
        for course in courses:
            button = tk.Button(self.buttons_frame, text=course,  # Ajouter les boutons au nouveau cadre
                               command=lambda course=course: self.select_course(self.controller, course))
            button.pack()

    def select_course(self, controller, course):
        """
        Sélectionne un cours, le stocke dans le contrôleur, ajoute le cours à la base de données
        et navigue vers la page d'attente des étudiants.

        Paramètres
        ----------
        controller : App
            L'instance de contrôleur de l'application.
        course : str
            Le nom du cours sélectionné.
        """
        # On met à jour le cours sélectionné dans le contrôleur
        controller.selected_course = course
        
        insert_course(controller.selected_course,datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime("%H:%M:%S"), "",controller.selected_master,) 
        
        # On passe à la page suivante
        controller.show_frame(StudentPage)
