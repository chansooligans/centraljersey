# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    my_dict = {'insert_me':"Hello I am from views.py !"}
    return render(request, 'mapapp/index.html', context=my_dict)

def testmapp(request):
    return render(request, 'wawa.html')