# Assigning Simulator
A simulator of assigning classrooms to courses using Python and SQLite.

# Method and Technical Description
The project is built with sqlite3 database that holds the courses, students, and classrooms tables.
* The database filename is classes.db.
* Python modules are create_db.py and schedule.py

## Database Structure
The database classes.db has three tables:
* **courses**: This table holds information of the courses.
* **students**: This table holds the number of students per grade.
* **classrooms**: This table holds the location and the status of each class room.

## schedule
This module is in charge of orchestrating the schedule of the courses.
It runs in a loop until one of the following conditions hold:
1. The database file schedule.db does not exist.
2. All courses are done (The courses table is empty).

## create_ db
This module is the module that builds the database and inputs the initial data from the
configuration file. When run, it will be given an argument of the path for the config file. For
example, python3 create_db.py config.

## Configuration Files
Each line in the configuration file represents either a course( C ), students( S ), or a
classroom( R ).
For example:
“C, 1, SPL 191, cs_ungrd, 80, 3, 2” represents a course id is 1, named “SPL 191” requires 80
computer science undergraduate students, located at classroom with id 3 and needs 2 iterations to 
complete , and
“S, cs_grad, 150” represents there are 150 computer science graduate students
“R, 1, 90/233” represents the classroom 90/ 233 whose id is 1.

### Built With
- OOP
- DAO, DTO Design Pattern

### Tech
* [Python](https://www.python.org/)
* [PyCharm](https://www.jetbrains.com/pycharm/)
* [Github](https://github.com/)

### Authors
* Amit Levizky
* Evgeny Kaidrikov
