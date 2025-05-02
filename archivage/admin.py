from django.contrib import admin
from .models import Categorie, Document, Historique

admin.site.register(Categorie)
admin.site.register(Document)
admin.site.register(Historique)