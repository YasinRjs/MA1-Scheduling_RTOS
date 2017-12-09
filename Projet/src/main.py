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
        j = 0
        while j < len(task_list) and keepGoing:
            if (timer > 0) :
                newTaskArrivalCalcul = jobs_list[j] * period_list[j] + offset_list[j] == timer
                taskDeadlineCalcul = (deadline_job[j]-1) * period_list[j] + deadline_list[j] + offset_list[j] == timer

            if (offset_list[j] < timer and taskDeadlineCalcul):
                if (toDo_list[j] >= wcet_list[j]):
                    keepGoing = False
                    if (withPrint):
                        print("timeInstant: Job T"+str(nums_list[j])+"J"+str(jobs_list[j])+" misses a deadline")
                else:
                    if (withPrint and keepGoing):
                        print(timer,": Deadline of job T"+str(nums_list[j])+"J"+str(deadline_job[j]))
                    deadline_job[j] += 1
            # ARRIVAL OR DEADLINE MISS
            if (keepGoing and offset_list[j] <= timer and newTaskArrivalCalcul):
                if (toDo_list[j] != 0):
                    if (withPrint):
                        print("timeInstant: Job T"+str(nums_list[j])+"J"+str(jobs_list[j])+" misses a deadline")
                    keepGoing = False
                else:
                    if (timer != end):
                        jobs_list[j] += 1
                        if (withPrint):
                            print(timer,": Arrival of job T"+str(nums_list[j])+"J"+str(jobs_list[j]))
                    toDo_list[j] = wcet_list[j]
            # DEADLINE
            j+=1

        if (keepGoing):
            highPriority = 0
            while (highPriority < len(task_list) and toDo_list[highPriority] == 0):
                highPriority+=1

            lastExecTime = timer
            if (highPriority < len(task_list)):
                canContinueExecuting = True
                while (toDo_list[highPriority] != 0 and canContinueExecuting):
                    toDo_list[highPriority] -= 1
                    timer += 1
                    k = 0
                    while canContinueExecuting and k<len(task_list):
                        newTaskArrivalCalcul = offset_list[k] + jobs_list[k] * period_list[k] == timer
                        taskDeadlineCalcul = jobs_list[k] * period_list[k]+deadline_list[k] + offset_list[k] == timer
                        if (offset_list[k] <= timer and newTaskArrivalCalcul) or \
                            (offset_list[k] < timer and taskDeadlineCalcul):
                            canContinueExecuting = False
                        k+=1
                if (withPrint):
                    if (timer <= end):
                        print(str(lastExecTime)+"-"+str(timer)+": T"+str(nums_list[highPriority])+"J"+str(jobs_list[highPriority]))
                    elif (lastExecTime != end):
                        print(str(lastExecTime)+"-"+str(end)+": T"+str(nums_list[highPriority])+"J"+str(jobs_list[highPriority]))
            else:
                timer+=1

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
