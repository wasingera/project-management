import csv
from classes import *

def readProjects(file):
    projects = []
    with open(file) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data = [row[0]] + [float(x) for x in row[1:]]
            proj = Project(*data)
            projects.append(proj)

    return projects

def readPeople(file):
    people = []

    with open(file) as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            name = row[2]
            email = row[1]
            grade = int(row[3])
            prevExp = row[6]
            prevLeader = row[7]
            leaderApp = row[8]
            major = row[9]
            choices = row[4:6]

            data = [name, email, grade, prevExp, prevLeader, leaderApp, major, choices]

            for i in range(3,7):
                if data[i] == 'Yes':
                    data[i] = 1
                else:
                    data[i] = 0

            p = Person(*data)
            people.append(p)

    return people
def placePerson(p):
    for c in p.choices:
        if c.isEmptySlot():
            c.assigned.append(p)
            break

        compare, i = c.getMinWeight()
        pWeight = c.calcWeight(p)

        if weight > compare[0]:
            old = assigned[i]
            c.assigned[i] = p
            placePerson(temp)
            break

def encodeChoices(person, projectNames):

    l = len(person.choices)
    for i in range(0, l):
        person.choices[i] = projectNames[person.choices[i]]

def match(person, projects):
    for c in person.choices:
        choice = projects[c]
        if choice.isEmptySlot():
            choice.assigned.append(person)
            break

        pWeight = choice.calcWeight(person)

        mWeight, index = choice.getLowest()

        if pWeight > mWeight:
            replaced = choice.assigned[index]
            choice.assigned[index] = person
            match(replaced, projects)
            break

def findMatches():

    # initialize projects
    projects = readProjects("projects.csv")

    people = readPeople("people.csv")

    for p in projects:
        print(p)

    print()

    projectNames = {}

    for i in range(0, len(projects)):
        name = projects[i].name
        projectNames[name] = i

    for p in people:
        encodeChoices(p, projectNames)

    for p in people:
        match(p, projects)

    for proj in projects:
        print(proj.name)
        for p in people:
            print(p.name, proj.calcWeight(p))
        print()

    return projects
