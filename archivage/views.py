from django.shortcuts import render
from .models import Document, Categorie

def accueil(request):
    return render(request, 'archivage/accueil.html')

def liste_documents(request):
    documents = Document.objects.all()
    return render(request, 'archivage/liste_documents.html', {'documents': documents})

def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'archivage/liste_categories.html', {'categories': categories})