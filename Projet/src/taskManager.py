
class TaskManager():

    def __init__(self, task_list, start=0, end=0, withPrint=False, audsley=False, lowestPriorityTasks=[]):
        self.task_list = task_list
        self.totalTasks = len(task_list)
        self.withPrint = withPrint
        self.start = start
        self.end = end
        self.period_list = self.getPeriodList()
        self.wcet_list = self.getWcetList()
        self.offset_list = self.getOffsetList()
        self.deadline_list = self.getDeadlineList()
        self.nums_list = self.getIdList()
        self.toDo_list = [0 for i in range(self.totalTasks)]
        self.jobs_list = [0 for i in range(self.totalTasks)]
        self.deadline_job = [1 for i in range(self.totalTasks)]
        self.listPlot = [0 for i in range(self.end)]
        self.audsley = audsley
        self.lowestPriorityTasks = lowestPriorityTasks

    def getPeriodList(self):
        return [task.getPeriod() for task in self.task_list]

    def getOffsetList(self):
        return [task.getOffset() for task in self.task_list]

    def getWcetList(self):
        return [task.getWcet() for task in self.task_list]

    def getDeadlineList(self):
        return [task.getDeadline() for task in self.task_list]

    def getIdList(self):
        return [task.getID() for task in self.task_list]

    def findP(self):
        return self.lcmOfPeriodList()

    def findOmax(self):
        return max(self.offset_list)

    def lcmOfPeriodList(self):
        res = 1
        for num in self.period_list:
            res = self.lcm(num, res)
        return res

    def lcm(self, a, b):
        res = a
        while (res%b)!=0:
            res += a
        return res

    def getNewTaskArrival(self, timer, taskIndex):
        return (self.jobs_list[taskIndex] * self.period_list[taskIndex] + self.offset_list[taskIndex] == timer) and self.offset_list[taskIndex] <= timer

    def getPlotList(self):
        return self.listPlot

    def getTaskDeadline(self, timer, taskIndex):
        return ((self.deadline_job[taskIndex]-1) * self.period_list[taskIndex] + self.deadline_list[taskIndex] + self.offset_list[taskIndex] == timer)

    def printDeadlineJob(self, timer, taskIndex):
        if (self.withPrint and self.start <= timer):
            print(timer,": Deadline of job T"+str(self.nums_list[taskIndex])+"J"+str(self.deadline_job[taskIndex]))

    def printDeadlineMiss(self, timer, taskIndex):
        if (self.withPrint and self.start <= timer):
            print(timer,": Job T"+str(self.nums_list[taskIndex])+"J"+str(self.jobs_list[taskIndex])+" misses a deadline")

    def printNewArrival(self, timer, taskIndex):
        if (self.withPrint and self.start <= timer):
            print(timer,": Arrival of job T"+str(self.nums_list[taskIndex])+"J"+str(self.jobs_list[taskIndex]+1))

    def printExecution(self, lastExecTime, timer, taskIndex):
        if (self.withPrint and self.start <= timer):
            if (timer <= self.end):
                print(str(lastExecTime)+"-"+str(timer)+": T"+str(self.nums_list[taskIndex])+"J"+str(self.jobs_list[taskIndex]))
            elif (lastExecTime != self.end):
                print(str(lastExecTime)+"-"+str(self.end)+": T"+str(self.nums_list[taskIndex])+"J"+str(self.jobs_list[taskIndex]))

    def arrivalOrMiss(self, newTaskArrivalCalcul, noDeadlineMiss):
        return (noDeadlineMiss and newTaskArrivalCalcul)

    def taskHasWork(self, taskIndex):
        return self.toDo_list[taskIndex] != 0

    def addNewJob(self, taskIndex):
        self.toDo_list[taskIndex] = self.wcet_list[taskIndex]

    def checkLowestPriorities(self, taskIndex):
        return self.task_list[taskIndex].getID() not in self.lowestPriorityTasks

    def launch(self):
        timer = 0
        noDeadlineMiss = True
        while (timer <= self.end and noDeadlineMiss):
            taskIndex = 0
            while (taskIndex < self.totalTasks and noDeadlineMiss):
                newTaskArrival = self.arrivalOrMiss(self.getNewTaskArrival(timer, taskIndex), noDeadlineMiss)
                deadlineOrMiss = self.getTaskDeadline(timer, taskIndex)

                # Is there a Miss or a new deadline ?
                if (deadlineOrMiss):
                    # Is it a miss ?
                    if (self.taskHasWork(taskIndex)):
                        if (not self.audsley):
                            self.printDeadlineMiss(timer, taskIndex)
                            noDeadlineMiss = False
                        else:
                            if (self.checkLowestPriorities(taskIndex)):
                                noDeadlineMiss = False
                    # It's a new deadline to print
                    else:
                        self.printDeadlineJob(timer, taskIndex)
                        self.deadline_job[taskIndex] += 1
                # Is there new Arrival or deadline Miss with the arrival
                if (newTaskArrival):
                    if (timer != self.end):
                        self.printNewArrival(timer, taskIndex)
                        self.jobs_list[taskIndex] += 1
                    self.addNewJob(taskIndex)
                taskIndex+=1

            # Continue until new event
            if (noDeadlineMiss):
                highPriority = 0
                while (highPriority < self.totalTasks and self.toDo_list[highPriority] == 0):
                    highPriority+=1

                lastExecTime = timer
                if (highPriority < self.totalTasks):
                    canContinueExecuting = True
                    while (self.taskHasWork(highPriority) and canContinueExecuting):
                        if timer<self.end:
                            self.listPlot[timer] = self.task_list[highPriority].getID()
                        self.toDo_list[highPriority] -= 1
                        timer += 1
                        taskIndex = 0
                        while (canContinueExecuting and taskIndex<self.totalTasks):
                            newTaskArrival = self.arrivalOrMiss(self.getNewTaskArrival(timer, taskIndex), noDeadlineMiss)
                            deadlineOrMiss = self.getTaskDeadline(timer, taskIndex)
                            if (newTaskArrival or deadlineOrMiss):
                                canContinueExecuting = False
                            taskIndex+=1
                    self.printExecution(lastExecTime, timer, highPriority)
                else:
                    timer+=1

        return noDeadlineMiss
