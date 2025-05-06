from django.db import models

from django.utils.timezone import now

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.nom

class Document(models.Model):
    VISIBILITE_CHOICES = [
        ('publique', 'Publique'),
        ('privee', 'Privée'),
        ('restreinte', 'Restreinte'),
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

class Historique(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="historiques", verbose_name="Document")
    action = models.CharField(max_length=50, verbose_name="Action", choices=[
        ('ajout', 'Ajout'),
        ('modification', 'Modification'),
        ('suppression', 'Suppression'),
        ('consultation', 'Consultation'),
    ])
    utilisateur = models.CharField(max_length=100, verbose_name="Utilisateur")
    date_action = models.DateTimeField(auto_now_add=True, verbose_name="Date de l'action")

    def __str__(self):
        return f"{self.action} - {self.document.titre} par {self.utilisateur}"
