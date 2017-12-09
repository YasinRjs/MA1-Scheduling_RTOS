class Task():
    def __init__(self,id, offset, period, deadline, wcet):
        self.id = id
        self.offset = offset
        self.period = period
        self.deadline = deadline
        self.wcet = wcet

    def __str__(self):
        return "\tOffset : " + self.offset + "\n\tPeriod : " + self.period + \
            "\n\tDeadline : " + self.deadline + "\n\tWcet : " + self.wcet

    def getID(self):
        return int(self.id)

    def getPeriod(self):
        return int(self.period)

    def getOffset(self):
        return int(self.offset)

    def getWcet(self):
        return int(self.wcet)

    def getDeadline(self):
        return int(self.deadline)
