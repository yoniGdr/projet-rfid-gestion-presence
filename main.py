import tkinter as tk
from pages import TeacherPage, MasterChoicePage, CoursesChoicePage, StudentPage, ListPage

class App(tk.Tk):
    """
    La classe App est le contrôleur principal de l'application et gère la navigation entre différentes pages.

    Elle hérite de la classe tk.Tk de la bibliothèque tkinter qui fournit une interface pour la bibliothèque de boîte à outils Tk.

    Attributs
    ---------
    current_page : str
        Le nom de la page actuellement affichée.
    frames : dict
        Un dictionnaire qui mappe les noms des pages à leurs instances respectives.
    selected_master : str
        Le master sélectionné actuellement, utilisé pour gérer les états entre les différentes pages.
    selected_course : str
        Le cours actuellement sélectionné, utilisé pour gérer les états entre les différentes pages.
    """
    def __init__(self):
        """
        Initialise l'application.
        """
        tk.Tk.__init__(self)
        self.title("scanner")
        self.geometry("320x240")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.current_page = None
        self.frames = {}
        
        self.selected_master = None   # Initialize selected_master
        self.selected_course = None   # Initialize selected_course
        
        # Créez une instance de chaque page et la stocke dans le dictionnaire self.frames
        for Page in (TeacherPage, MasterChoicePage, CoursesChoicePage, StudentPage ,ListPage):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        # Affiche la première page
        self.show_frame(TeacherPage)
        
    def show_frame(self, page_class):
        """
        Affiche une page spécifique.

        Paramètres
        ----------
        page_class : tk.Frame
            La classe de la page à afficher.

        Cette méthode met à jour l'attribut current_page, exécute la méthode 'refresh' si la page en contient une,
        et démarre le balayage RFID si la page a une méthode 'start_scanning'.
        """
        frame = self.frames[page_class.__name__]
        if hasattr(frame, 'refresh'):  # Vérifie si la page a une méthode 'refresh'
            frame.refresh()  # Si oui, l'appelle avant d'afficher la page
        frame.tkraise()
        self.current_page = page_class.__name__
        if hasattr(frame, 'start_scanning'):
            frame.start_scanning()


if __name__ == "__main__":
    app = App()
    app.mainloop()
