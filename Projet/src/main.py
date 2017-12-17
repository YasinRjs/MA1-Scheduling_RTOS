import sys

import itertools
import task
import parser
import taskManager
import systemGenerator
import plotScheduler
from copy import deepcopy
import numpy as np

NUMBEROFTASKS = 2

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

def isLowestPriorityViable(task_list, start, end, lowestPriorityTask):
    return simulate(task_list, start, end, False, True, lowestPriorityTask)

def printTaskIds(task_list):
    for task in task_list:
        print("Task",str(task.getID()), end=" ,")
    print()

def checkAudsley(totalTasks, task_list, start, end, lowestPriorityTask):
    if len(task_list) > 0:
        numberOfTab = totalTasks-(len(task_list)-1)
        new_task_list = deepcopy(task_list)
        new_task_list[lowestPriorityTask], new_task_list[-1] = new_task_list[-1], new_task_list[lowestPriorityTask]
        lowestPriorityTaskID = new_task_list[-1].getID()
        if (isLowestPriorityViable(new_task_list, start, end, lowestPriorityTaskID)):
            # On pourrait parcourir ici pour avoir un print plus jolie.
            print(numberOfTab*"\t" + "Task " + str(lowestPriorityTaskID)+" is lowest priority viable")
            for j in range(len(task_list)-1):
                checkAudsley(totalTasks, new_task_list[:-1], start, end, j)
        else:
            print(numberOfTab*"\t"+"Task "+str(lowestPriorityTaskID)+" is not lowest priority viable")

def audsley():
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    testFile = sys.argv[4]
    #########################################
    # Get tasks from file
    parse = parser.Parser(testFile)
    task_list = parse.getTaskList()
    printTasks(task_list)
    totalTasks = len(task_list)-1
    #########################################
    # TODO Can I launch it with this ?
    for i in range(len(task_list)):
        checkAudsley(totalTasks, task_list, start, end, i)

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
