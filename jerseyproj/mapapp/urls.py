from mapapp import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('testmapp/', views.testmapp, name='testmapp'),
]