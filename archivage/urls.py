# filepath: c:\Users\MAEVA\Desktop\VARBAF ARCHIVAGE\archivage\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),  # Page d'accueil
    path('documents/', views.liste_documents, name='documents'),  # Liste des documents
    path('documents/<int:document_id>/telecharger/', views.telecharger_document, name='telecharger_document'),
    path('categories/', views.liste_categories, name='categories'),  # Liste des catégories
    path('categories/<int:categorie_id>/', views.documents_par_categorie, name='documents_par_categorie'),
        path('historique/', views.afficher_historique, name='afficher_historique'),
]