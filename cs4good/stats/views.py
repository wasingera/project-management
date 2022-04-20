from django.shortcuts import render, redirect
from django.http import HttpResponse

from .funcs import readProjects, findMatches, makeRankings, makeFigs, total_dfs, makeTotFigs

# Create your views here.

def index(request):
    
    projects = makeRankings()

    choiceSeniority = makeTotFigs(projects)

    total_dfs(projects)

    
    return render(request, 'stats/index.html', { 'projects': projects, 'plot_div': choiceSeniority })


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

        return redirect("/")

    return render(request, 'stats/upload.html')

def project(request, project):
    projects = makeRankings()
    figs = makeFigs(projects)

    context = {
        'projects': projects,
        'proj': projects[project],
        'fig': figs[project],
    }
    return render(request, 'stats/project.html', context);

    return HttpResponse(projects[project])
    return HttpResponse('test')
