from django import forms
from .models import Categorie
from .models import Document
class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }
        labels = {
            'nom': 'Nom',
            'description': 'Description',
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['titre', 'categorie', 'fichier', 'description', 'responsable', 'visibilite']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du document'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'fichier': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responsable'}),
            'visibilite': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'titre': 'Titre',
            'categorie': 'Catégorie',
            'fichier': 'Fichier',
            'description': 'Description',
            'responsable': 'Responsable',
            'visibilite': 'Visibilité',
        }