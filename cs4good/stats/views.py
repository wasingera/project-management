from django.shortcuts import render
from django.http import HttpResponse
import os

# Create your views here.

def index(request):
    return HttpResponse('test')

def upload(request):
    if request.method == "POST":
        data = request.FILES['file']
        print(os.getcwd())
        with open('data.csv', 'wb') as file:
            for chunk in data.chunks():
                file.write(chunk)

        return HttpResponse("recieved")

    return render(request, 'stats/upload.html')
