def simulate(task_list, start, end):
    # TODO Optimize
    # TODO
    # TODO

    schedule_list = ["" for i in range(end)]
    forOutput = ["" for i in range(end)]

    period_list = getPeriodList(task_list)
    wcet_list = getWcetList(task_list)
    offset_list = getOffsetList(task_list)
    deadline_list = getDeadlineList(task_list)
    first = 0
    toDo_list = [0 for i in range(len(task_list))]

    for i in range(end):
        for j in range(len(task_list)):
            if (i%period_list[j] == 0 and offset_list[j] <= i):
                if (toDo_list[j] != 0):
                    print("timeInstant: Job T"+str(j+1),"J",str((i+1)//period_list[j]+1)," misses a deadline")
                    sys.exit(0)
                else:
                    print(i,": Arrival of job T"+str(j+1)+"J"+str((i+1)//period_list[j]+1))
                    toDo_list[j] = wcet_list[j]
            if (offset_list[j] <= i and i>=1 and i%deadline_list[j]==0):
                print(i,": Deadline of job T"+str(j+1)+"J"+str((i+1)//period_list[j]))

        print(i, " : " , toDo_list)
        highPriority = 0
        while (highPriority < len(task_list) and toDo_list[highPriority] == 0):
            highPriority+=1
        if (highPriority < len(task_list)):
            schedule_list[i] = "T"+str(highPriority+1)
            toDo_list[highPriority] -= 1

    print(schedule_list)










"""
import sys

from copy import deepcopy
import itertools
import task

def parseTasks(filename):
    task_list = []
    f = open(filename)
    lines = f.readlines()
    i = 1
    for line in lines:
        line = line.split(" ")
        offset = line[0]
        period = line[1]
        deadline = line[2]
        wcet = line[3]
        task_list.append(task.Task(i, offset, period, deadline, wcet))
        i+=1
    return task_list

def printTasks(task_list):
    print("#########################################################")
    for i in range(len(task_list)):
        print("Task " + str(i+1))
        print(str(task_list[i]))
    print("#########################################################")

def checkArgs(args):
    if len(args) < 3:
        print("ERROR : Missing arguments ..")
        sys.exit()

def lcm(a, b):
    res = a
    while (res%b)!=0:
        res += a
    return res

def lcmOfList(period_list):
    res = 1
    for num in period_list:
        res = lcm(num, res)
    return res

def getPeriodList(task_list):
    return [task.getPeriod() for task in task_list]

def getOffsetList(task_list):
    return [task.getOffset() for task in task_list]

def getWcetList(task_list):
    return [task.getWcet() for task in task_list]

def getDeadlineList(task_list):
    return [task.getDeadline() for task in task_list]

def getIdList(task_list):
    return [task.getID() for task in task_list]

def findP(task_list):
    period_list = getPeriodList(task_list)
    return lcmOfList(period_list)

def findOmax(task_list):
    offset_list = getOffsetList(task_list)
    return max(offset_list)

def findStudyInterval(task_list):
    """
        Using formula [O_max , O_max + 2 * P]
    """
    # First find P
    P = findP(task_list)
    # Then find O_max
    O_max = findOmax(task_list)

    return [O_max, O_max + 2*P]

def simulate(task_list, start, end, withPrint):
    schedule_list = ["" for i in range(end)]
    forOutput = ["" for i in range(end)]
    period_list = getPeriodList(task_list)
    wcet_list = getWcetList(task_list)
    offset_list = getOffsetList(task_list)
    deadline_list = getDeadlineList(task_list)
    first = 0
    toDo_list = [0 for i in range(len(task_list))]
    i = 0
    keepGoing = True
    while i <= end and keepGoing:
        j = 0
        while j < len(task_list) and keepGoing:
            if (i%period_list[j] == 0 and offset_list[j] <= i):
                if (toDo_list[j] != 0):
                    if (withPrint):
                        print("timeInstant: Job T"+str(task_list[j].getID()),"J",str((i+1)//period_list[j]+1)," misses a deadline")
                    keepGoing = False
                else:
                    if (withPrint and i != end):
                        print(i,": Arrival of job T"+str(task_list[j].getID())+"J"+str((i+1)//period_list[j]+1))
                    toDo_list[j] = wcet_list[j]
            j+=1
        if (keepGoing):
            for j in range(len(task_list)):
                if (offset_list[j] <= i and i>0 and i%deadline_list[j]==0):
                    if (withPrint):
                        print(i,": Deadline of job T"+str(task_list[j].getID())+"J"+str((i+1)//period_list[j]))

            highPriority = 0
            while (highPriority < len(task_list) and toDo_list[highPriority] == 0):
                highPriority+=1

            if (highPriority < len(task_list)):
                execTimeGiven = 0
                canContinueExecuting = True
                while (canContinueExecuting):
                    execTimeGiven += 1
                    toDo_list[highPriority] -= 1
                    k = 0
                    if (toDo_list[highPriority] == 0):
                        canContinueExecuting = False
                    while canContinueExecuting and k < highPriority:
                        if (((i+execTimeGiven)%period_list[k]==0 and offset_list[k] <= (i+execTimeGiven)) or \
                            (offset_list[k] <= (i+execTimeGiven) and ((i+execTimeGiven)%deadline_list[k])==0)):
                            canContinueExecuting = False
                        k+=1
                if (withPrint):
                    if (i+execTimeGiven <= end):
                        print(str(i)+"-"+str(i+execTimeGiven)+": T"+str(task_list[highPriority].getID())+"J"+str(((i+1)//period_list[highPriority]+1)))
                    elif (i != end):
                        print(str(i)+"-"+str(end)+": T"+str(task_list[highPriority].getID())+"J"+str(((i+1)//period_list[highPriority])+1))
                i+=execTimeGiven
            else:
                i+=1
    return keepGoing

def fact(num):
    return math.factorial(num)

def priorityViable():
    taskNum = int(sys.argv[2])
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    testFile = sys.argv[5]
    #########################################
    # Get tasks from file
    task_list = parseTasks(testFile)
    #########################################

    if (taskNum > 0 and taskNum <= len(task_list)):
        if (isLowestPriorityViable(task_list, start, end, 0, taskNum-1)):
            print("Yes,", task_list[taskNum-1].getID(), "is lowest-priority-viable.")
        else:
            print("No,", task_list[taskNum-1].getID(), "is not lowest-priority-viable.")
    else:
        print("Task number", taskNum, "doesn't exist !")

def isLowestPriorityViable(task_list, start, end, order, taskNum):
    tmp = task_list[order]
    task_list[order] = task_list[taskNum]
    task_list[taskNum] = tmp

    if (len(task_list) > 1):
        allPossiblePermutation = list(itertools.permutations(task_list[(order+1):]))
    else:
        allPossiblePermutation = task_list

    found = False
    i = 0
    while (i < len(allPossiblePermutation) and not found):
        new_task_list = task_list[:(order+1)] + [elem for elem in allPossiblePermutation[i]]
        found = simulate(new_task_list, start, end, False)
        i += 1

    return (not found)

def checkAudsley(task_list, start, end, current, taskIndexes):
    print(taskIndexes)
    for i in taskIndexes:
        print(task_list[i].getID())
    for i in taskIndexes:
        res = isLowestPriorityViable(task_list, start, end, current, i)
        if (res):
            print("\t"*current+"Task "+str(task_list[i].getID())+" is lowest priority viable")
            new_task_index = deepcopy(taskIndexes)
            new_task_list = deepcopy(task_list)
            new_task_list[i], new_task_list[current] = new_task_list[current], new_task_list[i]
            new_task_index.remove(i)
            checkAudsley(new_task_list, start, end, current+1, new_task_index)
        else:
            print("\t"*current+"Task "+str(task_list[i].getID())+" is not lowest priority viable")

def audsley():
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    testFile = sys.argv[4]

    #########################################
    # Get tasks from file
    task_list = parseTasks(testFile)
    #########################################
    checkAudsley(task_list, start, end, 0, [i for i in range(len(task_list))])

"""        while (j < len(task_list)):
            found = isLowestPriorityViable(task_list, start, end, j, i)
            if (found):
                print("Task "+str(task_list[j].getID())+" is lowest priority viable")
                found = False
            else:
                j+=1
"""

def main():
    #########################################
    # ARGS
    checkArgs(sys.argv)
    action = sys.argv[1]
    #########################################

    if action == "interval":
        testFile = sys.argv[2]
        #########################################
        # Get tasks from file and print
        task_list = parseTasks(testFile)
        printTasks(task_list)
        #########################################
        studyInterval = findStudyInterval(task_list)
        print("Study Interval of given tasks : ", studyInterval)
    elif action == "sim":
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        testFile = sys.argv[4]
        #########################################
        # Get tasks from file and print
        task_list = parseTasks(testFile)
        printTasks(task_list)
        print("\t->Tasks are ordered by decreasing priorities")
        print("Schedule from", start, "to", end, ";", len(task_list), "tasks.")
        #########################################
        canBeSimulated = simulate(task_list, start, end, True)
    elif action == "priorityViable":
        priorityViable()
    elif action == "audsley":
        audsley()


if __name__ == "__main__":
    main()
"""






















"""
import sys

import itertools
import task

def parseTasks(filename):
    task_list = []
    f = open(filename)
    lines = f.readlines()
    i = 0
    for line in lines:
        line = line.split(" ")
        offset = line[0]
        period = line[1]
        deadline = line[2]
        wcet = line[3]
        task_list.append(task.Task(i+1, offset, period, deadline, wcet))
        i+=1
    return task_list

def printTasks(task_list):
    print("#########################################################")
    for i in range(len(task_list)):
        print("Task " + str(i+1))
        print(str(task_list[i]))
    print("#########################################################")

def checkArgs(args):
    if len(args) < 3:
        print("ERROR : Missing arguments ..")
        sys.exit()

def lcm(a, b):
    res = a
    while (res%b)!=0:
        res += a
    return res

def lcmOfList(period_list):
    res = 1
    for num in period_list:
        res = lcm(num, res)
    return res

def getPeriodList(task_list):
    return [task.getPeriod() for task in task_list]

def getOffsetList(task_list):
    return [task.getOffset() for task in task_list]

def getWcetList(task_list):
    return [task.getWcet() for task in task_list]

def getDeadlineList(task_list):
    return [task.getDeadline() for task in task_list]

def getIdList(task_list):
    return [task.getID() for task in task_list]

def findP(task_list):
    period_list = getPeriodList(task_list)
    return lcmOfList(period_list)

def findOmax(task_list):
    offset_list = getOffsetList(task_list)
    return max(offset_list)

def findStudyInterval(task_list):
    """
        Using formula [O_max , O_max + 2 * P]
    """
    # First find P
    P = findP(task_list)
    # Then find O_max
    O_max = findOmax(task_list)

    return [O_max, O_max + 2*P]

def simulate(task_list, start, end, withPrint):
    schedule_list = ["" for i in range(end)]
    forOutput = ["" for i in range(end)]
    period_list = getPeriodList(task_list)
    wcet_list = getWcetList(task_list)
    offset_list = getOffsetList(task_list)
    deadline_list = getDeadlineList(task_list)
    first = 0
    toDo_list = [0 for i in range(len(task_list))]
    i = 0
    keepGoing = True
    while i <= end and keepGoing:
        j = 0
        while j < len(task_list) and keepGoing:
            if (i%period_list[j] == 0 and offset_list[j] <= i):
                if (toDo_list[j] != 0):
                    if (withPrint):
                        print("timeInstant: Job T"+str(task_list[j].getID()),"J",str((i+1)//period_list[j]+1)," misses a deadline")
                    keepGoing = False
                else:
                    if (withPrint and i != end):
                        print(i,": Arrival of job T"+str(task_list[j].getID())+"J"+str((i+1)//period_list[j]+1))
                    toDo_list[j] = wcet_list[j]
            j+=1
        if (keepGoing):
            for j in range(len(task_list)):
                if (offset_list[j] <= i and i>0 and i%deadline_list[j]==0):
                    if (withPrint):
                        print(i,": Deadline of job T"+str(task_list[j].getID())+"J"+str((i+1)//period_list[j]))

            highPriority = 0
            while (highPriority < len(task_list) and toDo_list[highPriority] == 0):
                highPriority+=1

            if (highPriority < len(task_list)):
                execTimeGiven = 0
                canContinueExecuting = True
                while (canContinueExecuting):
                    execTimeGiven += 1
                    toDo_list[highPriority] -= 1
                    k = 0
                    if (toDo_list[highPriority] == 0):
                        canContinueExecuting = False
                    while canContinueExecuting and k < highPriority:
                        if (((i+execTimeGiven)%period_list[k]==0 and offset_list[k] <= (i+execTimeGiven)) or \
                            (offset_list[k] <= (i+execTimeGiven) and ((i+execTimeGiven)%deadline_list[k])==0)):
                            canContinueExecuting = False
                        k+=1
                if (withPrint):
                    if (i+execTimeGiven <= end):
                        print(str(i)+"-"+str(i+execTimeGiven)+": T"+str(task_list[highPriority].getID())+"J"+str(((i+1)//period_list[highPriority]+1)))
                    elif (i != end):
                        print(str(i)+"-"+str(end)+": T"+str(task_list[highPriority].getID())+"J"+str(((i+1)//period_list[highPriority])+1))
                i+=execTimeGiven
            else:
                i+=1
    return keepGoing

def fact(num):
    return math.factorial(num)

def isLowestPriorityViable(task_list, start, end, taskNum):
    tmp = task_list[0]
    task_list[0] = task_list[taskNum]
    task_list[taskNum] = tmp

    if (len(task_list) > 1):
        allPossiblePermutation = list(itertools.permutations(task_list[1:]))
    else:
        allPossiblePermutation = task_list

    found = False
    i = 0
    while (i < len(allPossiblePermutation) and not found):
        new_task_list = [task_list[0]] + [elem for elem in allPossiblePermutation[i]]
        found = simulate(new_task_list, start, end, False)
        i += 1

    return found

def priorityViable():
    taskNum = int(sys.argv[2])
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    testFile = sys.argv[5]
    #########################################
    # Get tasks from file
    task_list = parseTasks(testFile)
    #########################################
    if (taskNum > 0 and taskNum <= len(task_list)):
        if (isLowestPriorityViable(task_list, start, end, taskNum-1)):
            print("Yes,", taskNum, "is lowest-priority-viable.")
        else:
            print("No,", taskNum, "is not lowest-priority-viable.")
    else:
        print("Task number", taskNum, "doesn't exist !")

def audlsey():
    pass

def main():
    #########################################
    # ARGS
    checkArgs(sys.argv)
    action = sys.argv[1]
    #########################################

    if action == "interval":
        testFile = sys.argv[2]
        #########################################
        # Get tasks from file and print
        task_list = parseTasks(testFile)
        printTasks(task_list)
        #########################################
        studyInterval = findStudyInterval(task_list)
        print("Study Interval of given tasks : ", studyInterval)
    elif action == "sim":
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        testFile = sys.argv[4]
        #########################################
        # Get tasks from file and print
        task_list = parseTasks(testFile)
        printTasks(task_list)
        print("\t->Tasks are ordered by decreasing priorities")
        print("Schedule from", start, "to", end, ";", len(task_list), "tasks.")
        #########################################
        canBeSimulated = simulate(task_list, start, end, True)
    elif action == "priorityViable":
        priorityViable()
    elif action == "audsley":
        audsley()



if __name__ == "__main__":
    main()
"""




























"""
import sys

import itertools
import task

def parseTasks(filename):
    task_list = []
    f = open(filename)
    lines = f.readlines()
    i = 0
    for line in lines:
        line = line.split(" ")
        offset = line[0]
        period = line[1]
        deadline = line[2]
        wcet = line[3]
        task_list.append(task.Task(i+1, offset, period, deadline, wcet))
        i+=1
    return task_list

def printTasks(task_list):
    print("#########################################################")
    for i in range(len(task_list)):
        print("Task " + str(i+1))
        print(str(task_list[i]))
    print("#########################################################")

def checkArgs(args):
    if len(args) < 3:
        print("ERROR : Missing arguments ..")
        sys.exit()

def lcm(a, b):
    res = a
    while (res%b)!=0:
        res += a
    return res

def lcmOfList(period_list):
    res = 1
    for num in period_list:
        res = lcm(num, res)
    return res

def getPeriodList(task_list):
    return [task.getPeriod() for task in task_list]

def getOffsetList(task_list):
    return [task.getOffset() for task in task_list]

def getWcetList(task_list):
    return [task.getWcet() for task in task_list]

def getDeadlineList(task_list):
    return [task.getDeadline() for task in task_list]

def getIdList(task_list):
    return [task.getID() for task in task_list]

def findP(task_list):
    period_list = getPeriodList(task_list)
    return lcmOfList(period_list)

def findOmax(task_list):
    offset_list = getOffsetList(task_list)
    return max(offset_list)

def findStudyInterval(task_list):
    """
        Using formula [O_max , O_max + 2 * P]
    """
    # First find P
    P = findP(task_list)
    # Then find O_max
    O_max = findOmax(task_list)

    return [O_max, O_max + 2*P]

def simulate(task_list, start, end, withPrint):
    schedule_list = ["" for i in range(end)]
    forOutput = ["" for i in range(end)]
    period_list = getPeriodList(task_list)
    wcet_list = getWcetList(task_list)
    offset_list = getOffsetList(task_list)
    deadline_list = getDeadlineList(task_list)
    first = 0
    toDo_list = [0 for i in range(len(task_list))]
    i = 0
    keepGoing = True
    while i <= end and keepGoing:
        j = 0
        while j < len(task_list) and keepGoing:
            if (i%period_list[j] == 0 and offset_list[j] <= i):
                if (toDo_list[j] != 0):
                    if (withPrint):
                        print("timeInstant: Job T"+str(task_list[j].getID()),"J",str((i+1)//period_list[j]+1)," misses a deadline")
                    keepGoing = False
                else:
                    if (withPrint and i != end):
                        print(i,": Arrival of job T"+str(task_list[j].getID())+"J"+str((i+1)//period_list[j]+1))
                    toDo_list[j] = wcet_list[j]
            j+=1
        if (keepGoing):
            for j in range(len(task_list)):
                if (offset_list[j] <= i and i>0 and i%deadline_list[j]==0):
                    if (withPrint):
                        print(i,": Deadline of job T"+str(task_list[j].getID())+"J"+str((i+1)//period_list[j]))

            highPriority = 0
            while (highPriority < len(task_list) and toDo_list[highPriority] == 0):
                highPriority+=1

            if (highPriority < len(task_list)):
                execTimeGiven = 0
                canContinueExecuting = True
                while (canContinueExecuting):
                    execTimeGiven += 1
                    toDo_list[highPriority] -= 1
                    k = 0
                    if (toDo_list[highPriority] == 0):
                        canContinueExecuting = False
                    while canContinueExecuting and k < highPriority:
                        if (((i+execTimeGiven)%period_list[k]==0 and offset_list[k] <= (i+execTimeGiven)) or \
                            (offset_list[k] <= (i+execTimeGiven) and ((i+execTimeGiven)%deadline_list[k])==0)):
                            canContinueExecuting = False
                        k+=1
                if (withPrint):
                    if (i+execTimeGiven <= end):
                        print(str(i)+"-"+str(i+execTimeGiven)+": T"+str(task_list[highPriority].getID())+"J"+str(((i+1)//period_list[highPriority]+1)))
                    elif (i != end):
                        print(str(i)+"-"+str(end)+": T"+str(task_list[highPriority].getID())+"J"+str(((i+1)//period_list[highPriority])+1))
                i+=execTimeGiven
            else:
                i+=1
    return keepGoing

def fact(num):
    return math.factorial(num)

def isLowestPriorityViable(task_list, start, end, taskIndex, rounds):
    tmp = task_list[taskIndex]
    task_list[taskIndex] = task_list[rounds]
    task_list[rounds] = tmp

    if (len(task_list) > 1):
        allPossiblePermutation = list(itertools.permutations(task_list[:rounds]))
    else:
        allPossiblePermutation = task_list

    for elem in allPossiblePermutation:
        print(getIdList(new_task_list))
        found = False
    i = 0
    while (i < len(allPossiblePermutation) and not found):
        new_task_list = [test for test in elem] + task_list[rounds:]
        found = simulate(new_task_list, start, end, False)
        i += 1

    return found

def priorityViable():
    taskNum = int(sys.argv[2])
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    testFile = sys.argv[5]
    #########################################
    # Get tasks from file
    task_list = parseTasks(testFile)
    id_list = getIdList(task_list)
    #########################################
    if (taskNum > 0 and taskNum <= len(task_list)):
        indexOfTaskNum = id_list.index(taskNum)
        lastElem = len(task_list)-1
        if (isLowestPriorityViable(task_list, start, end, indexOfTaskNum, lastElem)):
            print("Yes, Task", taskNum, "is lowest-priority-viable.")
        else:
            print("No, Task", taskNum, "is not lowest-priority-viable.")
    else:
        print("Task number", taskNum, "doesn't exist !")

def audlsey():
    pass

def main():
    #########################################
    # ARGS
    checkArgs(sys.argv)
    action = sys.argv[1]
    #########################################

    if action == "interval":
        testFile = sys.argv[2]
        #########################################
        # Get tasks from file and print
        task_list = parseTasks(testFile)
        printTasks(task_list)
        #########################################
        studyInterval = findStudyInterval(task_list)
        print("Study Interval of given tasks : ", studyInterval)
    elif action == "sim":
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        testFile = sys.argv[4]
        #########################################
        # Get tasks from file and print
        task_list = parseTasks(testFile)
        printTasks(task_list)
        print("\t->Tasks are ordered by decreasing priorities")
        print("Schedule from", start, "to", end, ";", len(task_list), "tasks.")
        #########################################
        canBeSimulated = simulate(task_list, start, end, True)
    elif action == "priorityViable":
        priorityViable()
    elif action == "audsley":
        audsley()



if __name__ == "__main__":
    main()
"""











"""
import sys

import itertools
import task
from copy import deepcopy
from random import randint

def parseTasks(filename):
    task_list = []
    f = open(filename)
    lines = f.readlines()
    i = 0
    for line in lines:
        line = line.split(" ")
        offset = line[0]
        period = line[1]
        deadline = line[2]
        wcet = line[3]
        task_list.append(task.Task(i+1, offset, period, deadline, wcet))
        i+=1
    return task_list

def printTasks(task_list):
    print("#########################################################")
    for i in range(len(task_list)):
        print("Task " + str(task_list[i].getID()))
        print(str(task_list[i]))
    print("#########################################################")

def checkArgs(args):
    if len(args) < 3:
        print("ERROR : Missing arguments ..")
        sys.exit()

def lcm(a, b):
    res = a
    while (res%b)!=0:
        res += a
    return res

def lcmOfList(period_list):
    res = 1
    for num in period_list:
        res = lcm(num, res)
    return res

def getPeriodList(task_list):
    return [task.getPeriod() for task in task_list]

def getOffsetList(task_list):
    return [task.getOffset() for task in task_list]

def getWcetList(task_list):
    return [task.getWcet() for task in task_list]

def getDeadlineList(task_list):
    return [task.getDeadline() for task in task_list]

def getIdList(task_list):
    return [task.getID() for task in task_list]

def findP(task_list):
    period_list = getPeriodList(task_list)
    return lcmOfList(period_list)

def findOmax(task_list):
    offset_list = getOffsetList(task_list)
    return max(offset_list)

def findStudyInterval(task_list):
    """
        Using formula [O_max , O_max + 2 * P]
    """
    # First find P
    P = findP(task_list)
    # Then find O_max
    O_max = findOmax(task_list)

    return [O_max, O_max + 2*P]

def simulate(task_list, start, end, withPrint):
    ############################################
    # LISTS
    period_list = getPeriodList(task_list)
    wcet_list = getWcetList(task_list)
    offset_list = getOffsetList(task_list)
    deadline_list = getDeadlineList(task_list)
    nums_list = getIdList(task_list)
    toDo_list = [0 for i in range(len(task_list))]
    jobs_list = [0 for i in range(len(task_list))]
    deadline_job = [1 for i in range(len(task_list))]
    ############################################

    timer = 0
    keepGoing = True
    newTaskArrivalCalcul = True
    taskDeadlineCalcul = False

    while timer <= end and keepGoing:
        if (timer > 0) :
            newTaskArrivalCalcul = (jobs_list[j] * period_list[j] + offset_list[j] == timer) and (offset_list[j] < timer)
            taskDeadlineCalcul = ((deadline_job[j]-1) * period_list[j] + deadline_list[j] + offset_list[j] == timer) and (offset_list[j] <= timer)

        highPriority = 0
        gotHighPriority = False
        while (highPriority < len(task_list) and toDo_list[highPriority] == 0):
            highPriority+=1
        if highPriority < len(task_list):
            gotHighPriority = True

        k = 0
        deadlineMiss = False
        deadlineMiss2 = False
        arrivalJob = False
        deadlineOk = False
        canContinueExecuting = True
        while (canContinueExecuting and not (newTaskArrivalCalcul or taskDeadlineCalcul)):
            if gotHighPriority:
                toDo_list[highPriority] -= 1
                timer += 1
            k = 0
            while canContinueExecuting and k<len(task_list):
                newTaskArrivalCalcul = (offset_list[k] + jobs_list[k] * period_list[k] == timer) and (offset_list[k] < timer)
                taskDeadlineCalcul = (jobs_list[k] * period_list[k]+deadline_list[k] + offset_list[k] == timer) and (offset_list[k] <= timer)
                if newTaskArrivalCalcul:
                    if(toDo_list[k] != 0):
                        deadlineMiss2 = True
                    elif (timer != end):
                        arrivalJob = True
                    canContinueExecuting = False
                if taskDeadlineCalcul:
                    if (toDo_list[k] >= wcet_list[k]):
                        deadlineMiss = True
                    else:
                        deadlineOk = True
                    canContinueExecuting = False
                if not (taskDeadlineCalcul or newTaskArrivalCalcul):
                    k+=1
            if not (highPriority < len(task_list) and canContinueExecuting):
                timer += 1
            elif (toDo_list[highPriority] == 0):
                canContinueExecuting = False
        if (deadlineMiss):
            if (withPrint):
                print("timeInstant: Job T"+str(nums_list[k])+"J"+str(jobs_list[k])+" misses a deadline")
            keepGoing = False
        elif (deadlineOk):
            if (withPrint and keepGoing):
                print(timer,": Deadline of job T"+str(nums_list[k])+"J"+str(deadline_job[k]))
            deadline_job[k] += 1
        # ARRIVAL OR DEADLINE MISS
        if (deadlineMiss):
            if (withPrint):
                print("timeInstant: Job T"+str(nums_list[k])+"J"+str(jobs_list[k])+" misses a deadline")
            keepGoing = False
        elif (arrivalJob):
            jobs_list[kj] += 1
            if (withPrint):
                print(timer,": Arrival of job T"+str(nums_list[k])+"J"+str(jobs_list[k]))
            toDo_list[k] = wcet_list[k]
        # DEADLINE
    return keepGoing

def fact(num):
    return math.factorial(num)

def isLowestPriorityViable(task_list, start, end, taskIndex, rounds):
    task_list_new = deepcopy(task_list)
    tmp = task_list[taskIndex]
    task_list_new[taskIndex] = task_list[rounds]
    task_list_new[rounds] = tmp

    if (len(task_list) > 1):
        allPossiblePermutation = list(itertools.permutations(task_list_new[:rounds]))
    else:
        allPossiblePermutation = task_list

    found = False
    i = 0
    while (i < len(allPossiblePermutation) and not found):
        new_task_list = [liste for liste in allPossiblePermutation[i]] + task_list_new[rounds:]
        found = simulate(new_task_list, start, end, False)
        i += 1

    return found

def priorityViable():
    taskNum = int(sys.argv[2])
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    testFile = sys.argv[5]
    #########################################
    # Get tasks from file
    task_list = parseTasks(testFile)
    nums_list = getIdList(task_list)
    #########################################
    if (taskNum > 0 and taskNum <= len(task_list)):
        taskIndex = nums_list.index(taskNum)
        latest = len(task_list)-1
        if (isLowestPriorityViable(task_list, start, end, taskIndex, latest)):
            print("Yes, Task", taskNum, "is lowest-priority-viable.")
        else:
            print("No, Task", taskNum, "is not lowest-priority-viable.")
    else:
        print("Task number", taskNum, "doesn't exist !")

def audsley():
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    testFile = sys.argv[4]
    #########################################
    # Get tasks from file
    task_list = parseTasks(testFile)
    nums_list = getIdList(task_list)
    #########################################
    latest = len(task_list)-1
    # TODO Can I launch it with this ?
    for i in range(len(task_list)):
        checkAudsley(task_list, start, end, i, latest)

def checkAudsley(task_list, start, end, taskIndex, latest):
    if (latest == -1):
        print(getIdList(task_list))
    if (latest != -1):
        numberOfTab = (len(task_list)-1-latest)
        if (isLowestPriorityViable(task_list, start, end, taskIndex, latest)):
            print(numberOfTab*"\t" + "Task " + str(task_list[taskIndex].getID())+" is lowest priority viable")
            task_list_new = deepcopy(task_list)
            tmp = task_list_new[taskIndex]
            task_list_new[taskIndex] = task_list_new[latest]
            task_list_new[latest] = tmp
            for j in range(latest):
                checkAudsley(task_list_new, start, end, j, latest-1)
        else:
            print(numberOfTab*"\t"+"Task "+str(task_list[taskIndex].getID())+" is not lowest priority viable")

def initSimulation():
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    testFile = sys.argv[4]
    #########################################
    # Get tasks from file and print
    task_list = parseTasks(testFile)
    printTasks(task_list)
    print("\t->Tasks are ordered by decreasing priorities")
    print("Schedule from", start, "to", end, ";", len(task_list), "tasks.")
    #########################################
    canBeSimulated = simulate(task_list, start, end, True)
    if (canBeSimulated):
        print("\n--> Scheduling is OK.")
    else:
        print("\n--> Can't be Scheduled.")

def calculUtilization(task_list):
    res = 0
    for task in task_list:
        res += (task.getWcet() / task.getPeriod())

    return res * 100

def writeTasksInFile(task_list, newFile):
    f = open(newFile, "w+")
    for task in task_list:
        offset = str(task.getOffset())
        period = str(task.getPeriod())
        deadline = str(task.getDeadline())
        wcet = str(task.getWcet())
        f.write(offset+" "+period+" "+deadline+" "+wcet+"\n")
    f.close()
    print("--> "+newFile+" created with success !")

def generate():
    numberOftasks = int(sys.argv[2])
    utilization = int(sys.argv[3])
    newFile = sys.argv[4]

    notFound = True
    while (notFound):
        task_list = []
        for i in range(numberOftasks):
            offset = randint(0,300)
            period = randint(1,150)
            wcet = randint(1,period)
            deadline = randint(wcet, period)
            task_list.append(task.Task(i+1, str(offset), str(period), str(deadline), str(wcet)))
        if (calculUtilization(task_list) >= (utilization-1) and calculUtilization(task_list) <= (utilization+1)):
            notFound = False

    writeTasksInFile(task_list, newFile)



def main():
    #########################################
    # ARGS
    checkArgs(sys.argv)
    action = sys.argv[1]
    #########################################

    if action == "interval":
        testFile = sys.argv[2]
        #########################################
        # Get tasks from file and print
        task_list = parseTasks(testFile)
        printTasks(task_list)
        #########################################
        studyInterval = findStudyInterval(task_list)
        print("Study Interval of given tasks : ", studyInterval)
    elif action == "sim":
        initSimulation()
    elif action == "priorityViable":
        priorityViable()
    elif action == "audsley":
        audsley()
    elif action == "gen":
        generate()



if __name__ == "__main__":
    main()
"""
