import sqlite3
import atexit


#Data Transfer Object
import sys


class Course(object):
    def __init__(self, id, course_name, student, number_of_students, class_id, course_length):
        self.id=id
        self.course_name = course_name
        self.student = student
        self.number_of_students = number_of_students
        self.class_id = class_id
        self.course_length = course_length


class Student(object):
    def __init__(self, grade, count):
        self.grade = grade
        self.count = count


class Classroom(object):
    def __init__(self, id, location, current_course_id, current_course_time_left):
        self.id=id
        self.location = location
        self.current_course_id = current_course_id
        self.current_course_time_left = current_course_time_left



#Data Access Object


class _Courses:
    def __init__(self, conn):
        self._conn = conn


    def insert(self,course):
        self._conn.execute("""
        INSERT INTO courses (id, course_name, student, number_of_students, class_id, course_length)
        VALUES (?, ?, ?, ?, ?, ?)
        """, [course.id, course.course_name, course.student, course.number_of_students, course.class_id, course.course_length])


    def find(self, course_id):
        c = self._conn.cursor()
        c.execute("""
        SELECT id, course_name FROM courses WHERE id = ?
        """, [course_id])
        return Course(*c.fetchone())


    def print_table(self, list_of_tuples):
        for item in list_of_tuples:
            print(item)


    def get_all_courses(self):
        c = self._conn.cursor()
        all = c.execute("""
                SELECT * 
                FROM courses""").fetchall()
        return [Course(*raw) for raw in all]


    def get_free_classrooms(self):
        c = self._conn.cursor()
        all = c.execute("""
        SELECT * 
        FROM classrooms
        where current_course_id = 0 AND current_course_time_left = 0
        """)
        return [Classroom(*raw) for raw in all]


    def delete_course(self,id):
        self._conn.execute("""
        DELETE FROM courses WHERE id = ?
        """, [id])


    def get_course_name(self, id):
        name = self._conn.execute("""
                SELECT course_name FROM courses WHERE id = ?
                """, [id])
        name = name.fetchone()[0]
        return str(name)


class _Students:
    def __init__(self, conn):
        self._conn = conn

    def insert(self,student):
        self._conn.execute("""
        INSERT INTO students (grade, count)
        VALUES (?, ?)
        """, [student.grade, student.count])

    def find(self, student_grade):
        c = self._conn.cursor()
        c.execute("""
        SELECT grade,  count FROM students WHERE grade = ?
        """, [student_grade])
        return Student(*c.fetchone())


    def print_table(self, list_of_tuples):
        for item in list_of_tuples:
            print(item)


    def get_all_students(self):
        c = self._conn.cursor()
        all = c.execute("""
                SELECT * 
                FROM students""").fetchall()
        return [Student(*raw) for raw in all]


    def reduce_amount_students(self, reduce, grade):
        self._conn.execute("""
                UPDATE students
                SET count = count - ?
                where grade = ?
                """, [reduce, grade])

class _Classrooms:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, classroom):
        self._conn.execute("""
          INSERT INTO classrooms (id, location, current_course_id, current_course_time_left)
          VALUES (?, ?, ?, ?)
        """, [classroom.id, classroom.location, classroom.current_course_id, classroom.current_course_time_left])

    def find(self, classrooms_id):
        c = self._conn.cursor()
        c.execute("""
          SELECT id, location FROM classrooms WHERE id = ?
        """, [classrooms_id])
        return Classroom(*c.fetchone())


    def print_table(self, list_of_tuples):
        for item in list_of_tuples:
            print(item)

    def get_classrooms(self):
        c = self._conn.cursor()
        all = c.execute("""
                  SELECT * FROM classrooms
                """)
        return [Classroom(*raw) for raw in all]

    def assign_course_to_classroom(self, class_room_id, current_id, current_course_time):
        self._conn.execute("""
        UPDATE classrooms
        SET current_course_id = ?, current_course_time_left = ?
        where id = ?
        """, [current_id, current_course_time, class_room_id])


    def get_all_course_id_in_classrooms(self):
        c = self._conn.cursor()
        c.execute("""
                  SELECT courses* FROM courses JOIN classrooms on courses.id = classrooms.current_course_id
                """)
        return c.fetchall()

    def reduce_time_left(self, id):
        self._conn.execute("""
                   UPDATE classrooms
                   SET current_course_time_left = current_course_time_left - 1
                   where id = ?
                   """, [id])


    def set_zero_course_id(self, id):
        self._conn.execute("""
                   UPDATE classrooms
                   SET current_course_id = 0
                   where id = ?
                   """, [id])

class _Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('schedule.db')
        self.courses = _Courses(self._conn)
        self.students = _Students(self._conn)
        self.classrooms = _Classrooms(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE courses (
            id  INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL,
            student TEXT NOT NULL,
            number_of_students INTEGER NOT NULL,
            class_id INTEGER REFERENCES classrooms(id),
            course_length INTEGER NOT NULL);


            CREATE TABLE students (
            grade  TEXT PRIMARY KEY,
            count INTEGER NOT NULL);


            CREATE TABLE classrooms (
            id  INTEGER PRIMARY KEY,
            location TEXT NOT NULL,
            current_course_id INTEGER NOT NULL,
            current_course_time_left INTEGER NOT NULL
            );
        """)



    def print_all(self):
        c = self._conn.cursor()
        all_courses = c.execute("""
        SELECT * from courses
        """).fetchall()

        all_classrooms = c.execute("""
        SELECT * from classrooms
        """).fetchall()

        all_students = c.execute("""
        SELECT * from students
        """).fetchall()

        print("courses")
        repo.courses.print_table(all_courses)
        print("classrooms")
        repo.classrooms.print_table(all_classrooms)
        print("students")
        repo.students.print_table(all_students)


repo = _Repository()
atexit.register(repo._close)