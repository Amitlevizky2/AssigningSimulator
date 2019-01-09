from persistence import repo
import persistence
import sys

repo.create_tables()
fileHandle = open(sys.argv[1], 'r')
for line in fileHandle:
    fields = line.split(', ')
    fields[fields.__len__() - 1] = fields[fields.__len__() - 1].replace('\n', '')
    if fields[0].__eq__('S'):
        s = persistence.Student(fields[1], int(fields[2]))
        repo.students.insert(s)
    elif fields[0].__eq__('C'):
        c = persistence.Course(int(fields[1]), fields[2], fields[3], int(fields[4]), int(fields[5]), int(fields[6]))
        repo.courses.insert(c)
    else:
        r = persistence.Classroom(int(fields[1]), fields[2], 0, 0)
        repo.classrooms.insert(r)
fileHandle.close()

repo.print_all()