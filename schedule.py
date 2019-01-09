import os
import sqlite3

from persistence import repo

def main():
    #1
    def part_one():
        for course in all_courses:
            if course.class_id == classroom.id and classroom.current_course_id == 0:
                print("(" + str(iteration) + ") " + classroom.location + ": " + course.course_name + " is schedule to start")
                repo.classrooms.assign_course_to_classroom(classroom.id, course.id, course.course_length)
                classroom.current_course_id = course.id
                classroom.current_course_time_left = course.course_length
                repo.students.reduce_amount_students(course.number_of_students, course.student)


    conn = sqlite3.connect('schedule.db')
    all_courses = repo.courses.get_all_courses()
    all_classrooms = repo.classrooms.get_classrooms()
    all_students = repo.students.get_all_students()
    iteration = 0
    while os.path.isfile('schedule.db') and all_courses.__len__() != 0:
        #1
        for classroom in all_classrooms:
            if classroom.current_course_id == 0 and classroom.current_course_time_left == 0:
                part_one()


            elif classroom.current_course_id != 0 and classroom.current_course_time_left != 0:
                if classroom.current_course_time_left > 1:
                    print("(" + str(iteration) + ") " + classroom.location + ": " + "occupied by " + repo.courses.get_course_name(classroom.current_course_id))
                for course in all_courses:
                    if course.id == classroom.current_course_id:
                        classroom.current_course_time_left -= 1
                        repo.classrooms.reduce_time_left(classroom.id)


            if classroom.current_course_time_left == 0 and classroom.current_course_id != 0:
                print("(" + str(iteration) + ") " + classroom.location + ": " + repo.courses.get_course_name(classroom.current_course_id) + " is done")
                repo.classrooms.set_zero_course_id(classroom.id)
                repo.courses.delete_course(classroom.current_course_id)
                for course in all_courses:
                    if course.class_id == classroom.id:
                        all_courses.remove(course)
                        classroom.current_course_id=0
                        classroom.current_course_time_left = 0
                part_one()
        repo.print_all()
        iteration+=1

main()