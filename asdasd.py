import sqlite3
import atexit


#Data Transfer Object
class Course(object):
    def __init__(self, id, course_name, student, number_of_students, class_id, course_length):
        self.id=id
        self.course_name = course_name
        self.student = student
        self.number_of_students=number_of_students
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


class _Repository:
    def __init__(self):
        _conn = sqlite3.connect('schedual.db')
        self.courses = _Courses(self._conn)
        self.students = _Students(self._conn)
        self.classrooms = _Classrooms(self._conn)

    def _close(self):
        self._conn.commite()
        self._conn.close()

        def create_tables(self):
            self._conn.executescript("""
            CREATE TABLE courses (
                id  INTEGER PRIMARY KEY
                course_name TEXT NOT NULL
                student TEXT NOT NULL
                number_of_students INTEGER NOT NULL
                class_id INTEGER REFERENCES classrooms(id)
                course_length INTEGER NOT NULL);


                CREATE TABLE students (
                grade  INTEGER PRIMARY KEY
                count INTEGER NOT NULL);


                CREATE TABLE classrooms (
                id  INTEGER PRIMARY KEY
                location TEXT NOT NULL
                current_course_id INTEGER NOT NULL
                current_course_time_left INTEGER NOT NULL
                );
            """)


repo = _Repository()
atexit.register(repo._close)