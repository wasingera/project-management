from django.shortcuts import render
from django.http import HttpResponse
from .funcs import readProjects, findMatches, stats

# Create your views here.

def index(request):
    projects = findMatches()

    info = []

    for project in projects:
        years = stats(project)
        info.append(years)

    print(info)

    return render(request, 'stats/index.html', { 'projects': projects, 'info': info })

def upload(request):
    if request.method == "POST":
        print(request.FILES)
        projects = request.FILES['projects']
        people = request.FILES['people']

        with open('projects.csv', 'wb') as file:
            for chunk in projects.chunks():
                file.write(chunk)

        with open('people.csv', 'wb') as file:
            for chunk in people.chunks():
                file.write(chunk)

        return HttpResponse("recieved")

    return render(request, 'stats/upload.html')
