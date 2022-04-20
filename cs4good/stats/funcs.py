import csv

from .classes import *

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pandas import DataFrame

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
            state = row[-1]

            # consolidate data
            data = [name, email, grade, prevExp, prevLeader, leaderApp, major, choices, state]

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

def makeRankings():
    ''' creates list sorted by weight for a project with all applicants to club as entries'''
    projects = readProjects("projects.csv")
    people = readPeople("people.csv")

    projectNames = {}

    for i in range(0, len(projects)):
        name = projects[i].name
        projectNames[name] = i

    for proj in projects:
        for p in people:
            weight = proj.calcWeight(p)

            proj.assigned.append((p, weight))

        proj.assigned.sort(reverse=True, key=lambda x: x[1])
    return projects


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

def make_dfs(proj):

    df1 = DataFrame(columns = ['grade', 'frequency'])

    grades = {}

    minGrade = 2999

    for member in proj.assigned:
        if member[0].grade < minGrade:
            minGrade = member[0].grade

    for i in range(minGrade,minGrade+4):
        grades[str(i)] = 0
    

    for member in proj.assigned:
        if proj.name in member[0].choices:
            grades[str(member[0].grade)] += 1
                
    for key,value in grades.items():
        grade = {'grade':key, 'frequency':value}
        df1 = df1.append(grade, ignore_index = True)

    df2 = DataFrame(columns = ['Item','Frequency'])
    df2 = df2.append({'Item':'Want Leadership','Frequency':0}, ignore_index=True)
    df2 = df2.append({'Item':'Do Not Want Leadership','Frequency':0}, ignore_index=True)

    for member in proj.assigned:
        if proj.name in member[0].choices:
            if member[0].leaderApp == 1:
                df2.iat[0,1] += 1
            else:
                df2.iat[1,1] += 1

    df3 = DataFrame(columns = ['State','Frequency'])

    states = {}

    for member in proj.assigned:
        if proj.name in member[0].choices:
            states[member[0].state] = 0
    
    for member in proj.assigned:
        if proj.name in member[0].choices:
            states[member[0].state] += 1
    
    for key,value in states.items():
        df3 = df3.append({'State':key,'Frequency':value}, ignore_index=True)

    return df1,df2,df3

def makeFigs(projects):
    
    figs = []
    numRows = 2
    numCols = 2

    for proj in projects:
        df1,df2,df3 = make_dfs(proj)

        fig = make_subplots(rows = numRows,
                            cols = numCols,
                            start_cell= 'top-left', 
                            specs=[[{'type': 'xy'},
                                    {'type': 'pie'}],
                                    [{'type': 'choropleth'},
                                    {'type': 'xy'}]],
                            subplot_titles=('Popularity Per Seniority', 
                                            'Number of Applicants Applying for Leadership',
                                            'Number of Applicants per State'))

        #Popularity By Seniority
        for grade,freq in df1.groupby('grade'):  
            fig.add_trace(go.Bar(x = freq['grade'], 
                                y = freq['frequency'], 
                                name = grade, 
                                hovertemplate="Grade = %{x}<br>Number of Applicants = %{y}<extra></extra>"),
                row=1, col=1)
                    
            fig.update_layout(legend_title_text = "grade")
            fig.update_xaxes(title_text="Seniority")
            fig.update_yaxes(title_text="Number of Applicants")
            fig.update_layout(showlegend=False, 
                              height = 800,
                              title_text= proj.name)
            fig.update_yaxes(automargin=True)
            fig.update_xaxes(automargin=True)
        
        #Number of Applicants Who Want Leadership

        fig.add_trace(go.Pie(   labels = df2['Item'],
                                values = df2['Frequency'],
                                hovertemplate ="Choice = %{label}<br>Applicants = %{value}<extra></extra>"),
                        row = 1, col = 2)

        fig.update_layout(legend_title_text = "Choice")
        fig.update_layout(showlegend=False, 
                            height = 800,
                            title_text= proj.name)
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)

        
        #Number of Applicants Per State
        for state,freq in df3.groupby('State'):
            fig.add_trace(go.Choropleth(showscale=False,
                                        locationmode = "USA-states", 
                                        locations = freq['State'], 
                                        z = freq['Frequency'],
                                        autocolorscale = True,
                                        name = state,
                                        colorscale = 'blues',
                                        colorbar = dict(xanchor='left', yanchor='bottom'),
                                        hovertemplate = "State = %{location}<br>Applicants = %{z}<extra></extra>"),
                          row = 2, col = 1)
         
            fig.update_layout(height = 800,
                              title_text= proj.name,
                              geo = dict(scope='usa',
                                         projection=go.layout.geo.Projection(type = 'albers usa'),
                                         showlakes=True))

            fig.update_yaxes(automargin=True)
            fig.update_xaxes(automargin=True)
        
        HTMLfig = fig.to_html(full_html=False)

        figs.append(HTMLfig)

    return figs
