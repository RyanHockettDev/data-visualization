from django.shortcuts import render

def home(request):
    return render(request, "home.html")
def dash(request):
    return render(request, "dash.html")