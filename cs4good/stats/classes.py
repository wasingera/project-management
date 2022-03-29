class Project:

    weights = 5

    # define class attributes
    def __init__(self, name, grade, prevExp, prevLeader, leaderApp, major, spots):
        self.name = name
        self.grade = grade
        self.prevExp = prevExp
        self.prevLeader = prevLeader
        self.leaderApp = leaderApp
        self.major = major
        self.spots = spots
        self.assigned = []

    # W = SUM( w * x ) / n -- weighted average
    # Do formula with weights
    def calcWeight(self, person):
        s = self.grade * person.grade + self.prevExp * person.prevExp + self.prevLeader * person.prevLeader + self.leaderApp * person.leaderApp + self.major * person.major

        return s / self.weights

    # get the lowest weight applicant and its index
    def getLowest(self):
        # weight, index
        low = (self.calcWeight(self.assigned[0]), 0)

        for i in range(1, len(self.assigned)):
            w = self.calcWeight(self.assigned[i])
            if w < low[0]:
                low = (w, i)

        return low

    # check if their is an empty spot on project
    def isEmptySlot(self):
        if len(self.assigned) < self.spots:
            return True
        return False

    # print out the matches
    def printMatches(self):
        print(self.name)
        for p in self.assigned:
            print("(%s, %s)  " % (p.name, self.calcWeight(p)))
        print()

    def __str__(self):
        # format for printing class attributes
        s = "%s, %s, %s, %s, %s, %s, %s, %s" % (self.name, self.grade, self.prevExp, self.prevLeader, self.leaderApp, self.major, self.spots, self.assigned)
        return s

class Person:
    # define person attributes
    def __init__(self, name, email, grade, prevExp, prevLeader, leaderApp, major, choices):
        self.name = name
        self.email = email
        self.grade = grade
        self.prevExp = prevExp
        self.prevLeader = prevLeader
        self.leaderApp = leaderApp
        self.major = major
        self.choices = choices

    def __str__(self):
        # format for printing attributes
        s = "%s, %s, %s, %s, %s, %s, %s, %s" % (self.name, self.email, self.grade, self.prevExp, self.prevLeader, self.leaderApp, self.major, self.choices)
        return s
