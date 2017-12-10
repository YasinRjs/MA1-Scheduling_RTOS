import task

class Parser():

    def __init__(self, filename, task_list = [], write = False):
        if (write):
            self.task_list = task_list
            self.newFile = filename
        else:
            self.task_list = self.parseTasks(filename)

    def parseTasks(self, filename):
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


    def writeTasksInFile(self):
        f = open(self.newFile, "w+")
        for task in self.task_list:
            offset = str(task.getOffset())
            period = str(task.getPeriod())
            deadline = str(task.getDeadline())
            wcet = str(task.getWcet())
            f.write(offset+" "+period+" "+deadline+" "+wcet+"\n")
        f.close()
        print("--> "+self.newFile+" created with success !")

    def getTaskList(self):
        return self.task_list
