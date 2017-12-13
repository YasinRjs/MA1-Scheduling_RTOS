import matplotlib.pyplot as plt
import numpy as np

class PlotScheduler():
    def __init__(self, listPlot, totalTasks):
        self.listPlot = listPlot
        self.totalTasks = totalTasks
        self.matrixTasks = [[0 for i in range(len(listPlot))] for j in range(self.totalTasks)]

    def avg(self, a, b):
        return (a + b) / 2.0

    def preprocess(self):
        newList = []
        for i in range(1, self.totalTasks+1):
            listSchedul = [j for j, x in enumerate(self.listPlot) if x==i]
            newList.append(listSchedul)
        return newList

    def to_xy(self, liste):
        x, y = [], []
        for i in range(len(self.matrixTasks)):
            y.extend([i]*len(liste[i]))
            x.extend(liste[i])
        x, y = np.array(x), np.array(y)
        return x,y

    def plot(self):
        liste = self.preprocess()
        x,y = self.to_xy(liste)
        labels = np.array(["Task "+str(i+1) for i in range(self.totalTasks)])
        plt.hlines(y, x, x+1, lw = 2, color = 'red')
        plt.ylim(max(y)+0.5, min(y)-0.5)
        plt.yticks(range(y.max()+1), labels)
        plt.show()
