from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
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

    def clean_categorie(self):
        categorie = self.cleaned_data.get('categorie')
        if not categorie:
            raise forms.ValidationError("Veuillez sélectionner une catégorie.")
        return categorie

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Prénom')
    last_name = forms.CharField(max_length=30, required=True, label='Nom')

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        
        if commit:
            user.save()
            # Ajouter l'utilisateur au groupe "Utilisateurs limités"
            limited_users_group, _ = Group.objects.get_or_create(name='Utilisateurs limités')
            user.groups.add(limited_users_group)
            # Donner des permissions de base
            user.is_staff = True  # Permet l'accès à l'interface d'administration
            user.save()
        
        return user