from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categorie(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.nom

class Document(models.Model):
    VISIBILITE_CHOICES = [
        ('publique', 'Publique'),
        ('privee', 'Privée'),
    ]

    titre = models.CharField(max_length=200, verbose_name="Titre du document")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="documents", verbose_name="Catégorie")
    fichier = models.FileField(upload_to="documents/", verbose_name="Fichier")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    responsable = models.CharField(max_length=100, verbose_name="Responsable")
    visibilite = models.CharField(max_length=20, choices=VISIBILITE_CHOICES, default='publique', verbose_name="Visibilité")
    # date_ajout = models.DateTimeField(auto_now_add=True, default=now)  # Ajoutez default=now
    def __str__(self):
        return self.titre

    def est_accessible(self, user):
        """
        Vérifie si un utilisateur peut accéder au document
        """
        if self.visibilite == 'publique':
            return True
        return user.is_authenticated

class Historique(models.Model):
    TYPE_CHOICES = [
        ('document', 'Document'),
        ('categorie', 'Catégorie'),
        ('utilisateur', 'Utilisateur'),
    ]
    
    ACTION_CHOICES = [
        # Actions sur les documents
        ('ajout_document', 'Ajout de document'),
        ('modification_document', 'Modification de document'),
        ('suppression_document', 'Suppression de document'),
        ('consultation_document', 'Consultation de document'),
        ('telechargement_document', 'Téléchargement de document'),
        # Actions sur les catégories
        ('ajout_categorie', 'Ajout de catégorie'),
        ('modification_categorie', 'Modification de catégorie'),
        ('suppression_categorie', 'Suppression de catégorie'),
        # Actions sur les utilisateurs
        ('ajout_utilisateur', 'Ajout d\'utilisateur'),
        ('suppression_utilisateur', 'Suppression d\'utilisateur'),
    ]

    type_element = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type d'élément", default='document')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, verbose_name="Action")
    date_action = models.DateTimeField(auto_now_add=True, verbose_name="Date de l'action")
    utilisateur = models.CharField(max_length=100, verbose_name="Utilisateur")
    
    # Champs optionnels pour stocker les détails de l'action
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="historiques")
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
    details = models.TextField(blank=True, null=True, verbose_name="Détails")

    class Meta:
        ordering = ['-date_action']
        verbose_name = "Historique"
        verbose_name_plural = "Historiques"

    def __str__(self):
        return f"{self.get_action_display()} - {self.date_action}"
