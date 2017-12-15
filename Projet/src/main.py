import sys

import itertools
import task
import parser
import taskManager
import systemGenerator
import plotScheduler
from copy import deepcopy
import numpy as np

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

def findStudyInterval(task_list):
    """
        Using formula [O_max , O_max + 2 * P]
    """
    taskManag = taskManager.TaskManager(task_list)
    # First find P
    P = taskManag.findP()
    # Then find O_max
    O_max = taskManag.findOmax()

    return [O_max, O_max + 2*P]

def simulate(task_list, start, end, withPrint, audsley=False, taskNum=0):
    ############################################
    # LISTS
    systemSimul = taskManager.TaskManager(task_list, start, end, withPrint, audsley, taskNum)
    res = systemSimul.launch()
    if (not audsley):
        if (res):
            print("\n--> Scheduling is OK.")
        else:
            print("\n--> Can't be Scheduled.")
        ############################################
        plotList = systemSimul.getPlotList()
        plotSched = plotScheduler.PlotScheduler(plotList, len(task_list))

        plotSched.plot()

    return res

def fact(num):
    return math.factorial(num)

def initSimulation():
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    testFile = sys.argv[4]
    #########################################
    # Get tasks from file and print
    parse = parser.Parser(testFile)
    task_list = parse.getTaskList()
    printTasks(task_list)
    print("\t->Tasks are ordered by decreasing priorities")
    print("Schedule from", start, "to", end, ";", len(task_list), "tasks.")
    #########################################
    simulate(task_list, start, end, True)

def generate():
    numberOfTasks = int(sys.argv[2])
    utilization = int(sys.argv[3])
    newFile = sys.argv[4]
    systemGen = systemGenerator.SystemGenerator(numberOfTasks, utilization)
    task_list = systemGen.getTaskList()
    parse = parser.Parser(newFile, task_list, True)
    parse.writeTasksInFile()

def isLowestPriorityViable(task_list, start, end, taskIndex, rounds, lowestPriorityTasks):
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
        found = simulate(new_task_list, start, end, False, True, lowestPriorityTasks)
        i += 1

    return found

def checkAudsley(task_list, start, end, taskIndex, latest, lowestPriorityTasks = []):
    if (latest == -1):
        print(getIdList(task_list))
    if (latest != -1):
        numberOfTab = (len(task_list)-1-latest)
        if (isLowestPriorityViable(task_list, start, end, taskIndex, latest, lowestPriorityTasks)):
            newLowestPriorityTasks = deepcopy(lowestPriorityTasks)
            newLowestPriorityTasks.append(task_list[taskIndex].getID())
            print(numberOfTab*"\t" + "Task " + str(task_list[taskIndex].getID())+" is lowest priority viable")
            task_list_new = deepcopy(task_list)
            tmp = task_list_new[taskIndex]
            task_list_new[taskIndex] = task_list_new[latest]
            task_list_new[latest] = tmp
            for j in range(latest):
                checkAudsley(task_list_new, start, end, j, latest-1, lowestPriorityTasks)
        else:
            print(numberOfTab*"\t"+"Task "+str(task_list[taskIndex].getID())+" is not lowest priority viable")

def audsley():
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    testFile = sys.argv[4]
    #########################################
    # Get tasks from file
    parse = parser.Parser(testFile)
    task_list = parse.getTaskList()
    printTasks(task_list)
    #########################################
    latest = len(task_list)-1
    # TODO Can I launch it with this ?
    for i in range(len(task_list)):
        checkAudsley(task_list, start, end, i, latest)

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
        parse = parser.Parser(testFile)
        task_list = parse.getTaskList()
        printTasks(task_list)
        #########################################
        studyInterval = findStudyInterval(task_list)
        print("Study Interval of given tasks : ", studyInterval)
    elif action == "sim":
        initSimulation()
    elif action == "audsley":
        audsley()
    elif action == "gen":
        generate()



if __name__ == "__main__":
    main()
