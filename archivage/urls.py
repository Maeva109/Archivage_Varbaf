# filepath: c:\Users\MAEVA\Desktop\VARBAF ARCHIVAGE\archivage\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('documents/', views.liste_documents, name='liste_documents'),
]