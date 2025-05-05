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
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/modifier/<int:categorie_id>/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/supprimer/<int:categorie_id>/', views.supprimer_categorie, name='supprimer_categorie'),
    path('documents/', views.liste_documents, name='liste_documents'),
    path('documents/ajouter/', views.ajouter_document, name='ajouter_document'),
    path('documents/modifier/<int:document_id>/', views.modifier_document, name='modifier_document'),
    path('documents/supprimer/<int:document_id>/', views.supprimer_document, name='supprimer_document'),
    path('admin-panel/categories/', views.liste_categories_admin, name='liste_categories_admin'),
    path('admin-panel/documents/', views.liste_documents_admin, name='liste_documents_admin'),
    path('admin-panel/utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
path('admin-panel/historique/', views.liste_historique, name='liste_historique'),
]