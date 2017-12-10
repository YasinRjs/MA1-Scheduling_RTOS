from random import randint
import task

class SystemGenerator():

    def __init__(self, numberOfTasks, utilization):
        self.task_list = self.generate(numberOfTasks, utilization)

    def getTaskList(self):
        return self.task_list

    def calculUtilization(self, task_list):
        res = 0
        for task in task_list:
            res += (task.getWcet() / task.getPeriod())

        return res * 100

    def generate(self, numberOfTasks, utilization):
        notFound = True
        while (notFound):
            task_list = []
            for i in range(numberOfTasks):
                offset = randint(0,300)
                period = randint(1,150)
                wcet = randint(1,period)
                deadline = randint(wcet, period)
                task_list.append(task.Task(i+1, str(offset), str(period), str(deadline), str(wcet)))
            if (self.calculUtilization(task_list) >= (utilization-1) and self.calculUtilization(task_list) <= (utilization+1)):
                notFound = False

        return task_list
