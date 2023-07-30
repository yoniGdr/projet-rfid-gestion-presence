from dataTools import *
import datetime

def get_student_attendance(card_id):
    """
    Get the attendance of a student by his card id.
    param: card_id: the card id of the student
    """
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("SELECT nom, prénom FROM Students WHERE card_id = ?", (card_id,))
    data = cur.fetchone()
    if data is None:
        print("Invalid student card id.")
        return
    
    student_name, student_prenom = data
    cur.execute(
        """SELECT Courses.module, Courses.class_date, Courses.class_hour_start, Courses.class_hour_end
        FROM Students, Attendance, Courses 
        WHERE Students.student_id = Attendance.student_id 
        AND Attendance.course_id = Courses.course_id
        AND Students.card_id = ?""",
        (card_id,),
    )

    rows = cur.fetchall()
    conn.close()

    if len(rows) == 0:
        print(f"{student_name} {student_prenom} n'a participé à aucun cours.")
    else:
        for row in rows:
            module, date, start_time, end_time = row
            print(f"{student_name} {student_prenom} a participé au cours de {module} le {date} de {start_time} à {end_time}.")
    

def main():
    conn = create_connection()

    card_id = input("Entrez l'ID de la carte de l'étudiant: ")
    master_name = 'Internet of things'
    
    get_student_attendance(card_id)

if __name__ == '__main__':
    main()
