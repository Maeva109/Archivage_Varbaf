from django.shortcuts import render, get_object_or_404, redirect
from .models import Document, Categorie, Historique, Document
from django.http import FileResponse
from django.db.models import Count
from django.contrib.auth.models import User
from .forms import CategorieForm, DocumentForm

def accueil(request):
    return render(request, 'archivage/accueil.html')

def liste_documents(request):
    visibilite = request.GET.get('visibilite', 'publique')  # Par défaut, affiche les documents publics
    documents = Document.objects.filter(visibilite=visibilite)
    return render(request, 'archivage/liste_documents.html', {'documents': documents, 'visibilite': visibilite})

def liste_documents_admin(request):
    documents = Document.objects.all()
    return render(request, 'archivage/liste_documents_admin.html', {'documents': documents})

def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'archivage/liste_categories.html', {'categories': categories})

def liste_categories_admin(request):
    categories = Categorie.objects.all()
    return render(request, 'archivage/liste_categories_admin.html', {'categories': categories})

def documents_par_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    documents = Document.objects.filter(categorie=categorie)
    return render(request, 'archivage/documents_par_categorie.html', {
        'categorie': categorie,
        'documents': documents
    })

def consulter_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    # Enregistrer l'action dans l'historique
    Historique.objects.create(
        document=document,
        action='consultation',
        utilisateur=request.user.username if request.user.is_authenticated else 'Anonyme',  # Gérer les utilisateurs non connectés
    )
    return render(request, 'archivage/consulter_document.html', {'document': document})

def afficher_historique(request):
    historique = Historique.objects.all().order_by('-date_action')
    return render(request, 'archivage/historique.html', {'historique': historique})

def test_historique(request):
    historique = Historique.objects.all()
    print(historique)  # Vérifiez si des entrées sont affichées dans la console
    return render(request, 'archivage/test.html', {'historique': historique})

def telecharger_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    # Enregistrer l'action dans l'historique
    Historique.objects.create(
        document=document,
        action='telechargement',
        utilisateur=request.user.username if request.user.is_authenticated else 'Anonyme',
    )
    return FileResponse(document.fichier.open(), as_attachment=True, filename=document.fichier.name)

def accueil(request):
    # Calcul des statistiques
    categories_count = Categorie.objects.count()
    documents_count = Document.objects.count()
    publique_count = Document.objects.filter(visibilite='publique').count()
    privee_count = Document.objects.filter(visibilite='privee').count()
    restreinte_count = Document.objects.filter(visibilite='restreinte').count()

    return render(request, 'archivage/accueil.html', {
        'categories_count': categories_count,
        'documents_count': documents_count,
        'publique_count': publique_count,
        'privee_count': privee_count,
        'restreinte_count': restreinte_count,
    })

def admin_dashboard(request):
    # Calcul des statistiques
    categories_count = Categorie.objects.count()
    documents_count = Document.objects.count()
    users_count = User.objects.count()
    historique_count = Historique.objects.count()

    return render(request, 'archivage/admin_dashboard.html', {
        'categories_count': categories_count,
        'documents_count': documents_count,
        'users_count': users_count,
        'historique_count': historique_count,
    })

# Vue pour ajouter une catégorie
def ajouter_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_categories')
    else:
        form = CategorieForm()
    return render(request, 'archivage/ajouter_categorie.html', {'form': form})

# Vue pour modifier une catégorie
def modifier_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return redirect('liste_categories')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'archivage/modifier_categorie.html', {'form': form})

# Vue pour supprimer une catégorie
def supprimer_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    if request.method == 'POST':
        categorie.delete()
        return redirect('liste_categories')
    return render(request, 'archivage/supprimer_categorie.html', {'categorie': categorie})

# Vue pour afficher la liste des documents
def liste_documents(request):
    documents = Document.objects.all()
    return render(request, 'archivage/liste_documents.html', {'documents': documents})

# Vue pour ajouter un document
def ajouter_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_documents')
    else:
        form = DocumentForm()
    return render(request, 'archivage/ajouter_document.html', {'form': form})

# Vue pour modifier un document
def modifier_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('liste_documents')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'archivage/modifier_document.html', {'form': form})

# Vue pour supprimer un document
def supprimer_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.delete()
        return redirect('liste_documents')
    return render(request, 'archivage/supprimer_document.html', {'document': document})

def liste_utilisateurs(request):
    utilisateurs = User.objects.all()
    return render(request, 'archivage/liste_utilisateurs.html', {'utilisateurs': utilisateurs})

def liste_historique(request):
    historique = Historique.objects.all()
    return render(request, 'archivage/liste_historique.html', {'historique': historique})