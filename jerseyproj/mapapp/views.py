# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    my_dict = {'insert_me':"Hello I am from views.py !"}
    return render(request, 'mapapp/index.html', context=my_dict)

def wawa(request):
    return render(request, 'maps/wawa.html')

def dunkin(request):
    return render(request, 'maps/dunkin.html')

def edu_college(request):
    return render(request, 'maps/edu_college.html')

def nfl_eagles(request):
    return render(request, 'maps/nfl_eagles.html')

def nfl_giants(request):
    return render(request, 'maps/nfl_giants.html')

def pork_pork_roll(request):
    return render(request, 'maps/pork_pork_roll.html')

def pork_taylor_ham(request):
    return render(request, 'maps/pork_taylor_ham.html')

def pob_native_jeresy(request):
    return render(request, 'maps/pob_native_jeresy.html')

def pob_foreigh_born(request):
    return render(request, 'maps/pob_foreigh_born.html')