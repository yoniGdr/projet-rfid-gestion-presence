# Fichier qui permet de générer la BDD.
import sqlite3
from sqlite3 import Error

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

def create_table_Students(conn):
    try:
        sql = ''' CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                prénom TEXT NOT NULL,
                card_id TEXT NOT NULL
            );'''
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def create_table_teachers(conn):
    try:
        sql = ''' CREATE TABLE IF NOT EXISTS Teachers (
                teacher_id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                prénom TEXT NOT NULL,
                card_id TEXT NOT NULL
            );'''
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def create_table_Courses(conn):
    try:
        sql = ''' CREATE TABLE IF NOT EXISTS Courses (
                course_id INTEGER PRIMARY KEY,
                master TEXT NOT NULL,
                module TEXT NOT NULL,
                class_date TEXT NOT NULL,
                class_hour_start TEXT NOT NULL,
                class_hour_end TEXT NOT NULL
            );'''
        c = conn.cursor()
        c.execute(sql) 
    except Error as e:
        print(e)

def create_table_Module(conn):
    try:
        sql = ''' CREATE TABLE IF NOT EXISTS Module (
                module_id INTEGER PRIMARY KEY,
                module_name TEXT NOT NULL,
                master TEXT NOT NULL
            );'''
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)



def create_table_Attendance(conn):
    try:
        sql = ''' CREATE TABLE IF NOT EXISTS Attendance (
                attendance_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                course_id INTEGER,
                attendance_status DEFAULT 0,
                FOREIGN KEY (student_id) REFERENCES Students (student_id),
                FOREIGN KEY (course_id) REFERENCES Courses (course_id)
            );'''
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def create_all_tables():
    database = create_connection()

    if database is not None:
        create_table_Students(database)
        create_table_teachers(database)
        create_table_Module(database)
        create_table_Courses(database)
        create_table_Attendance(database)

    else:
        print("Erreur! Impossible de créer la connexion à la base de données.")



def insert_student(student_name, student_prenom, card_id):
    database = create_connection()
    c = database.cursor()
    c.execute("INSERT INTO Students (nom, prénom, card_id) VALUES (?, ?, ?)", (student_name, student_prenom, card_id))
    database.commit()

def insert_all_students():
    insert_student("Yoni", "Gaudiere", "289382403748")

def insert_teacher(teacher_name, teacher_prenom, card_id):
    database = create_connection()
    c = database.cursor()
    c.execute("INSERT INTO Teachers (nom, prénom, card_id) VALUES (?, ?, ?)", (teacher_name, teacher_prenom, card_id))
    database.commit()

def insert_all_teachers():
    insert_teacher("Guesepe", "Lipari", "497440696002") 

def insert_module(module_name, master_name):
    database = create_connection()
    c = database.cursor()
    c.execute("INSERT INTO Module (module_name, master) VALUES (?, ?)", (module_name, master_name))
    database.commit()

def insert_all_modules():
    insert_module("ASA", "Internet of things")
    insert_module("COMPIL", "Internet of things")
    insert_module("HD", "Internet of things")
    insert_module("SDS", "Internet of things")
    
    insert_module("ASA", "Cloud computing")
    insert_module("COMPIL", "Cloud computing")
    insert_module("RESEAU", "Cloud computing")
    insert_module("SDS", "Cloud computing")

def insert_course(module, class_date, class_hour_start, class_hour_end, master_name):    
    database = create_connection()
    c = database.cursor()
    if master_name is not None:
        c.execute("INSERT INTO Courses (master, module, class_date, class_hour_start, class_hour_end) VALUES (?, ?, ?, ?, ?)", (master_name, module, class_date, class_hour_start, class_hour_end))
        database.commit()
    else:
        print("Master non trouvé")

def insert_attendance(student_id, course_id, attendance):
    database = create_connection()
    c = database.cursor()
    c.execute("INSERT INTO Attendance (student_id, course_id, attendance) VALUES (?, ?, ?)", (student_id, course_id, attendance))
    database.commit()

def main():
    
    database = create_connection()
    create_all_tables()
    insert_all_students()
    insert_all_modules()
    insert_all_teachers()
    print("Base de donnée chargé")

if __name__ == '__main__':
    main()
