# filepath: c:\Users\MAEVA\Desktop\VARBAF ARCHIVAGE\archivage\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),  # Page d'accueil
    path('documents/', views.liste_documents, name='documents'),  # Liste des documents
    path('categories/', views.liste_categories, name='categories'),  # Liste des catégories
]