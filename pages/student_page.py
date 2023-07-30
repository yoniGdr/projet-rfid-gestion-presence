import tkinter as tk
from tkinter import messagebox
from mfrc522 import SimpleMFRC522
from data import *
from dataTools import *
from .teacher_page import TeacherPage
from .list_page import ListPage

reader = SimpleMFRC522()

class StudentPage(tk.Frame):
    """
    Page affichée lors de la prise des présences.

    Attributs
    ----------
    parent : tk.Widget
        Le widget parent de cette page.
    controller : App
        L'instance de contrôleur de l'application.

    Méthodes
    --------
    scan_student_card()
        Vérifie si un tag RFID est détecté. Si oui, vérifie si c'est un étudiant ou un professeur et agit en conséquence.
    resume_scanning()
        Réinitialise le message d'information et recommence le scan.
    start_scanning()
        Met à jour le label du cours actuel et commence le scan.
    """
    def __init__(self, parent, controller):
        """
        Initialise la page d'attente des étudiants avec un label pour le cours actuel, un label 
        pour afficher des messages d'information, un bouton pour afficher la liste des présents, 
        et commence le scan des cartes.

        Paramètres
        ----------
        parent : tk.Widget
            Le widget parent de cette page.
        controller : App
            L'instance de contrôleur de l'application.
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db_conn = create_connection()
        
        self.current_course_label = tk.Label(self, text="")
        self.current_course_label.pack(side="top", fill="x", pady=10)
        
        self.label = tk.Label(self, text="En attente du scan d'un élève")
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.info_label = tk.Label(self, text="")  # affiche les messages d'information
        self.info_label.pack(side="top", fill="x", pady=10)
        self.scanning = True
        self.scan_student_card()
        
        list_button = tk.Button(self, text="liste",
                               command=lambda: controller.show_frame(ListPage))
        list_button.pack(side="right", anchor="sw") 


    def scan_student_card(self):
        """
        Vérifie si un tag RFID est détecté. Si c'est le cas, vérifie si c'est un étudiant 
        ou un professeur et agit en conséquence. Si c'est un étudiant, vérifie si sa carte 
        a déjà été scannée, et si ce n'est pas le cas, met à jour son statut de présence.
        Si c'est un professeur, demande s'il veut mettre fin au cours.

        Le scan est répété toutes les secondes si aucun tag n'est détecté.
        """
    
        if self.controller.current_page == 'TeacherPage':
            return
        if self.controller.current_page == 'MasterChoicePage':
            return
            
        id, text = reader.read_no_block()
        if is_student_id_valid(self.db_conn, str(id)):
            if has_student_already_scanned( str(id), self.controller.selected_course):
                self.info_label.config(text="Carte déja scannée")
            else:
                update_student_status(str(id), self.controller.selected_course)
                print(get_present_students(self.controller.selected_course))
                self.info_label.config(text="Carte validée")
            
            self.scanning = False 
            self.after(3000, self.resume_scanning)
            
        elif is_teacher_id_valid(self.db_conn, str(id)):
            result = messagebox.askyesno("Question", "Mettre fin au cours?")
            if result == True:
                end_course(self.controller.selected_course)
                self.controller.show_frame(TeacherPage)
            else:
                self.scan_student_card()
           
        else:
            self.after(1000, self.scan_student_card)
            
    def resume_scanning(self):
        """
        Réinitialise le message d'information et recommence le scan 3 secondes après qu'un tag a été détecté.
        """
        self.info_label.config(text="") 
        self.scanning = True  
        self.scan_student_card()  
            
    def start_scanning(self):
        """
        Met à jour le label du cours actuel et commence le scan.
        """
        self.current_course_label.config(text=f"Cours actuel: {self.controller.selected_course}")
        self.scan_student_card()
