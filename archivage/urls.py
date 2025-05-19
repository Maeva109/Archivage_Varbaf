# filepath: c:\Users\MAEVA\Desktop\VARBAF ARCHIVAGE\archivage\urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Pages publiques
    path('', views.accueil, name='accueil'),
    path('documents/', views.documents, name='documents'),
    path('categories/', views.liste_categories, name='categories'),
    path('categories/<int:categorie_id>/', views.documents_par_categorie, name='documents_par_categorie'),
    
    # Actions sur les documents
    path('documents/<int:document_id>/telecharger/', views.telecharger_document, name='telecharger_document'),
    path('documents/ajouter/', views.ajouter_document, name='ajouter_document'),
    path('documents/modifier/<int:document_id>/', views.modifier_document, name='modifier_document'),
    path('documents/supprimer/<int:document_id>/', views.supprimer_document, name='supprimer_document'),
    
    # Actions sur les catégories
    path('categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/modifier/<int:categorie_id>/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/supprimer/<int:categorie_id>/', views.supprimer_categorie, name='supprimer_categorie'),
    
    # Pages d'administration
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/categories/', views.liste_categories_admin, name='liste_categories_admin'),
    path('admin-panel/documents/', views.liste_documents_admin, name='liste_documents_admin'),
    path('admin-panel/documents/<int:document_id>/', views.consulter_document, name='consulter_document'),
    path('admin-panel/utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('admin-panel/utilisateurs/ajouter/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('admin-panel/utilisateurs/supprimer/<int:user_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('admin-panel/historique/', views.liste_historique, name='liste_historique'),
    
    # API
    path('api/categories/creer/', views.creer_categorie_api, name='creer_categorie_api'),
]