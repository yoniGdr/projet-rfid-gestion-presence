# Fichier contenant des fonctions utile pour interoger et modifié la BDD.
import sqlite3
from sqlite3 import Error
import datetime

def create_connection():
    """
    Crée une connexion à la base de données SQLite.

    Retourne
    --------
    conn : Connection
        L'objet de connexion à la base de données.
    """
    conn = None
    try:
        conn = sqlite3.connect('database.db')  
    except Error as e:
        print(e)

    if conn:
        return conn

def get_course_list_by_master(master_name):
    """
    Récupère la liste des modules pour un master spécifique.

    Paramètres
    ----------
    master_name : str
        Le nom du master pour lequel récupérer la liste des modules.

    Retourne
    --------
    course_list : list
        La liste des noms des modules pour le master donné.
    """
    database = create_connection()
    c = database.cursor()

    c.execute("SELECT DISTINCT module_name FROM Module WHERE master = ?", (master_name,))

    rows = c.fetchall()

    # Extraire uniquement les noms de cours des tuples retournés
    course_list = [row[0] for row in rows]

    return course_list
    
        
def update_student_status(card_id, module_name):
    """
    Met à jour le statut de présence d'un étudiant pour un cours spécifique.

    Paramètres
    ----------
    card_id : str
        L'identifiant de carte RFID de l'étudiant.
    module_name : str
        Le nom du module pour lequel mettre à jour le statut de présence.
    """
    conn = create_connection()
    cur = conn.cursor()
    
    # Récupérer l'ID de l'élève correspondant au card_id
    cur.execute("SELECT student_id FROM Students WHERE card_id = ?", (card_id,))
    student_id, = cur.fetchone()
    
    course_id = get_course_id(module_name)
    
    cur.execute("INSERT INTO Attendance (student_id, course_id, attendance_status) VALUES (?, ?, ?)",
                (student_id, course_id, 1))  # 1 pour "présent"
 
    conn.commit()
    conn.close()
    
def has_student_already_scanned(card_id, module_name):
    """
    Vérifie si un étudiant a déjà été enregistré pour un module spécifique.

    Paramètres
    ----------
    card_id : str
        L'identifiant de carte RFID de l'étudiant.
    module_name : str
        Le nom du module pour vérifier l'enregistrement.

    Retourne
    --------
    bool
        True si l'étudiant a déjà été enregistré, False sinon.
    """
    conn = create_connection()
    cur = conn.cursor()
    
     # Récupérer l'ID de l'élève correspondant au card_id
    cur.execute("SELECT student_id FROM Students WHERE card_id = ?", (card_id,))
    student_id, = cur.fetchone()
    
    course_id = get_course_id(module_name)

    cur.execute("""
    SELECT *
    FROM Attendance
    WHERE student_id = ? AND course_id = ?
    """, (student_id, course_id))

    # fetchone() renvoie None si aucune correspondance n'est trouvée
    record = cur.fetchone()

    return record is not None

    
def get_course_id(module_name):
    """
    Récupère l'ID d'un module.

    Paramètres
    ----------
    module_name : str
        Le nom du module pour lequel récupérer l'ID.

    Retourne
    --------
    course_id : int
        L'ID du module, ou None si aucun module ne correspond au nom donné.
    """
    conn = create_connection()
    cur = conn.cursor()
    course_date = datetime.datetime.now().strftime('%Y-%m-%d')
    cur.execute("SELECT course_id FROM Courses WHERE module = ? AND class_date = ?", (module_name, course_date))

    result = cur.fetchone()

    conn.close()

    if result:
        return result[0]  # renvoie le course_id
    else:
        return None  # si aucun cours ne correspond au module et à la date spécifiés

def get_present_students(module_name):
    """
    Récupère une liste des étudiants présents pour un module spécifique.

    Paramètres
    ----------
    module_name : str
        Le nom du module pour lequel récupérer la liste des étudiants présents.

    Retourne
    --------
    students : list of tuple
        La liste des étudiants présents pour le module donné, chaque étudiant étant un tuple (nom, prénom).
    """
    conn = create_connection()
    cur = conn.cursor()
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    cur.execute("""
    SELECT s.nom, s.prénom 
    FROM Students s 
    JOIN Attendance a ON s.student_id = a.student_id 
    JOIN Courses c ON a.course_id = c.course_id 
    WHERE a.attendance_status = 1 AND c.module = ? AND c.class_date = ? 
    """, (module_name, today))

    students = cur.fetchall()

    conn.close()

    return students
    
def get_master_name(conn):
    """
    Récupère une liste de tous les noms de master uniques.

    Paramètres
    ----------
    conn : Connection
        La connexion à la base de données.

    Retourne
    --------
    master_names : list
        La liste des noms de tous les masters.
    """
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT master FROM Module")

    rows = cur.fetchall()

    return [row[0] for row in rows]
    
    
def is_teacher_id_valid(conn, card_id):
    """
    Vérifie si un identifiant de carte RFID est valide pour un enseignant.

    Paramètres
    ----------
    conn : Connection
        La connexion à la base de données.
    card_id : str
        L'identifiant de carte RFID à vérifier.

    Retourne
    --------
    bool
        True si l'identifiant de carte est valide, False sinon.
    """
    query = "SELECT 1 FROM Teachers WHERE card_id = ?"
    c = conn.cursor()
    c.execute(query, (card_id,))
    result = c.fetchone()

    if result: 
        return True
    else:
        return False

def is_student_id_valid(conn, card_id):
    """
    Vérifie si un identifiant de carte RFID est valide pour un étudiant.

    Paramètres
    ----------
    conn : Connection
        La connexion à la base de données.
    card_id : str
        L'identifiant de carte RFID à vérifier.

    Retourne
    --------
    bool
        True si l'identifiant de carte est valide, False sinon.
    """
    query = "SELECT * FROM Students WHERE card_id = ?"
    c = conn.cursor()
    c.execute(query, (card_id,))
    result = c.fetchone()

    if result: 
        return True
    else:
        return False
        
def end_course(module_name):
    """
    Met fin à un cours en mettant à jour l'heure de fin dans la base de données.

    Paramètres
    ----------
    module_name : str
        Le nom du module pour lequel mettre fin au cours.
    """
    conn = create_connection()
    cur = conn.cursor()

    # Récupérer l'heure actuelle
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Mettre à jour l'heure de fin du cours
    cur.execute(
        """UPDATE Courses
        SET class_hour_end = ?
        WHERE module = ? AND class_date = ?""",
        (current_time, module_name, datetime.datetime.now().strftime('%Y-%m-%d')),
    )
    conn.commit()
    conn.close()
    print(f"Le cours {module_name} a été terminé à {current_time}.")


