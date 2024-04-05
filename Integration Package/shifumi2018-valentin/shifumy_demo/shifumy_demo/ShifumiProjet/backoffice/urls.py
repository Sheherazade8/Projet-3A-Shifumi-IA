
from django.contrib import admin
from django.urls import path,include
from . import  views



urlpatterns = [
    path('', views.home),
    path('Game', views.show),
    path('Analysis', views.analysis),
    path('thisGame', views.boardGame),
    path('AllGame', views.boardAllGame),

]
