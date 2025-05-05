from django.shortcuts import render, get_object_or_404
from .models import Document, Categorie, Historique, Document
from django.http import FileResponse
from django.db.models import Count
from django.contrib.auth.models import User

def accueil(request):
    return render(request, 'archivage/accueil.html')

def liste_documents(request):
    visibilite = request.GET.get('visibilite', 'publique')  # Par défaut, affiche les documents publics
    documents = Document.objects.filter(visibilite=visibilite)
    return render(request, 'archivage/liste_documents.html', {'documents': documents, 'visibilite': visibilite})
def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'archivage/liste_categories.html', {'categories': categories})

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