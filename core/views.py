from django.shortcuts import render

def index_view(request):
    return render(request, 'home.html')

def instructions(request):
    return render(request, 'instructions.html')
