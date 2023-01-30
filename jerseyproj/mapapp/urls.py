from mapapp import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('wawa/', views.wawa, name='wawa'),
    path('dunkin/', views.dunkin, name='dunkin'),
    path('edu_college/', views.edu_college, name='edu_college'),
    path('nfl_eagles/', views.nfl_eagles, name='nfl_eagles'),
    path('nfl_giants/', views.nfl_giants, name='nfl_giants'),
    path('pork_pork_roll/', views.pork_pork_roll, name='pork_pork_roll'),
    path('pork_taylor_ham/', views.pork_taylor_ham, name='pork_taylor_ham'),
    path('pob_native_jeresy/', views.pob_native_jeresy, name='pob_native_jeresy'),
    path('pob_foreigh_born/', views.pob_foreigh_born, name='pob_foreigh_born'),
]