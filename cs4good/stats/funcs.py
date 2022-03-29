import csv
from .classes import *

def readProjects(file):
    ''' takes in a csv filename, returns a list of projects'''

    projects = []
    with open(file) as f:
        reader = csv.reader(f)

        # skip title how
        next(reader)


        for row in reader:
            # pull data out of file
            # the first column is a string, so it can't be converted to float
            # instead we just append one list comprehension to another
            data = [row[0]] + [float(x) for x in row[1:]]

            # make a new project with data
            proj = Project(*data)

            # add to list of all projects
            projects.append(proj)

    # return list of all projects
    return projects

def readPeople(file):
    ''' takes in a csv filename, returns a list of people'''

    people = []

    with open(file) as f:
        # Open the csv file
        reader = csv.reader(f)

        # skip over the title row
        next(reader)

        for row in reader:
            # pull all the data out (might be better to turn into dictionary)
            name = row[2]
            email = row[1]
            grade = int(row[3])
            prevExp = row[6]
            prevLeader = row[7]
            leaderApp = row[8]
            major = row[9]
            choices = row[4:6]

            # consolidate data
            data = [name, email, grade, prevExp, prevLeader, leaderApp, major, choices]

            # replace text answers with integers so you can do algebra with them
            for i in range(3,7):
                if data[i] == 'Yes':
                    data[i] = 1
                else:
                    data[i] = 0

            # Make a new person object with the choice data
            p = Person(*data)

            # add new person to list of all applicants
            people.append(p)

    # return list of applicants
    return people

def placePerson(p):
    ''' Takes in a Person p, then puts them in one of their choices '''
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
    ''' turn project names into their index in the projects array '''
    l = len(person.choices)
    for i in range(0, l):
        person.choices[i] = projectNames[person.choices[i]]

def match(person, projects):
    ''' matches most qualified applicants with projects'''
    # TODO: change to match everybody with everything, then sort by weight

    # iterate over person's choices
    for c in person.choices:
        choice = projects[c]

        # if there's an open slot on one, add them to the project
        if choice.isEmptySlot():
            choice.assigned.append(person)
            break

        # otherwise calculate the weight of that person for the project
        pWeight = choice.calcWeight(person)

        # get index and weight of lowest applicant on project
        mWeight, index = choice.getLowest()

        # if current applicant is more qualified, then replace the less qualified
        if pWeight > mWeight:
            replaced = choice.assigned[index]
            choice.assigned[index] = person

            # now try to match the person we just removed
            match(replaced, projects)
            break

def findMatches():
    ''' returns list of projects with a filled applicants field '''

    # initialize projects
    projects = readProjects("projects.csv")

    people = readPeople("people.csv")

    for p in projects:
        print(p)

    print()

    projectNames = {}

    # create dict with name => index in array
    for i in range(0, len(projects)):
        name = projects[i].name
        projectNames[name] = i

    for p in people:
        encodeChoices(p, projectNames)

    for p in people:
        match(p, projects)

    # print out results (not needed in web app)
    # for proj in projects:
    #     print(proj.name)
    #     for p in people:
    #         print(p.name, proj.calcWeight(p))
    #     print()

    return projects
