from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # This loads your HTML file
