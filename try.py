fileHandle = open('/users/studs/bsc/2019/levamit/PycharmProjects/untitled1/kok.txt', 'r')

for line in fileHandle:
    fields = line.split(',')
    a = [0]*10
    fields[fields.__len__()-1] = fields[fields.__len__() - 1].replace('\n', '')
    i=0
    for item in fields:
        if item[0] == ' ':
            a.append(item[:0]+ "" +item[0:])
        else:
            a.append(item)

    print(a)

fileHandle.close()