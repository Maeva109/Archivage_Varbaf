from django.shortcuts import render, get_object_or_404, redirect
from .models import Document, Categorie, Historique
from django.http import FileResponse, JsonResponse
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CategorieForm, DocumentForm, CustomUserCreationForm
from django.contrib import messages
from django.db import models
from django.contrib.auth.hashers import make_password
import json
from django.urls import reverse

def accueil(request):
    # Calcul des statistiques
    categories_count = Categorie.objects.count()
    documents_count = Document.objects.count()
    publique_count = Document.objects.filter(visibilite='publique').count()
    privee_count = Document.objects.filter(visibilite='privee').count()
    restreinte_count = Document.objects.filter(visibilite='restreinte').count()

    # Gestion de la recherche rapide
    query = request.GET.get('q', '')
    documents = []
    if query:
        documents = Document.objects.filter(titre__icontains=query)

    return render(request, 'archivage/accueil.html', {
        'categories_count': categories_count,
        'documents_count': documents_count,
        'publique_count': publique_count,
        'privee_count': privee_count,
        'restreinte_count': restreinte_count,
        'documents': documents,
        'query': query,
    })

def liste_documents(request):
    query = request.GET.get('q', '')
    visibilite = request.GET.get('visibilite', '')
    
    if request.user.is_authenticated:
        documents = Document.objects.all()
    else:
        documents = Document.objects.filter(visibilite='publique')

    if query:
        documents = documents.filter(titre__icontains=query)
    if visibilite:
        if not request.user.is_authenticated and visibilite == 'privee':
            messages.warning(request, "Vous devez être connecté pour voir les documents privés.")
            documents = documents.none()
        else:
            documents = documents.filter(visibilite=visibilite)

    return render(request, 'archivage/liste_documents.html', {
        'documents': documents,
        'visibilite': visibilite,
        'peut_voir_prives': request.user.is_authenticated
    })

@login_required
def liste_documents_admin(request):
    query = request.GET.get('q', '')
    if query:
        documents = Document.objects.filter(titre__icontains=query)
    else:
        documents = Document.objects.all()
    return render(request, 'archivage/liste_documents_admin.html', {'documents': documents})

def liste_categories(request):
    query = request.GET.get('q', '')
    if query:
        categories = Categorie.objects.filter(nom__icontains=query)
    else:
        categories = Categorie.objects.all()
    return render(request, 'archivage/liste_categories.html', {'categories': categories})

@login_required
def liste_categories_admin(request):
    query = request.GET.get('q', '')
    if query:
        categories = Categorie.objects.filter(nom__icontains=query)
    else:
        categories = Categorie.objects.all()
    return render(request, 'archivage/liste_categories_admin.html', {'categories': categories})

def documents_par_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    
    # Filtrer les documents selon l'état de connexion de l'utilisateur
    if request.user.is_authenticated:
        # Les utilisateurs connectés peuvent voir tous les documents
        documents = Document.objects.filter(categorie=categorie)
    else:
        # Les utilisateurs non connectés ne peuvent voir que les documents publics
        documents = Document.objects.filter(categorie=categorie, visibilite='publique')
    
    return render(request, 'archivage/documents_par_categorie.html', {
        'categorie': categorie,
        'documents': documents,
        'peut_voir_prives': request.user.is_authenticated
    })

def consulter_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    
    # Vérifier si l'utilisateur peut accéder au document
    if not document.est_accessible(request.user):
        messages.error(request, "Vous devez être connecté pour accéder à ce document privé.")
        return redirect('documents')
        
    # Enregistrer l'action dans l'historique
    Historique.objects.create(
        document=document,
        action='consultation',
        utilisateur=request.user.username if request.user.is_authenticated else 'Anonyme',
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
    
    # Vérifier si l'utilisateur peut accéder au document
    if document.visibilite == 'privee' and not request.user.is_authenticated:
        messages.error(request, "Vous devez être connecté pour télécharger ce document privé.")
        return redirect('documents')
    
    # Enregistrer l'action dans l'historique
    Historique.objects.create(
        type_element='document',
        action='telechargement',
        utilisateur=request.user.username if request.user.is_authenticated else 'Anonyme',
        document=document,
        details=f"Téléchargement du document : {document.titre}"
    )
    
    return FileResponse(document.fichier.open(), as_attachment=True, filename=document.fichier.name)

@login_required
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

def is_admin(user):
    return user.is_superuser

# @user_passes_test(is_admin)
def ajouter_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            categorie = form.save()
            # Enregistrer dans l'historique
            Historique.objects.create(
                type_element='categorie',
                action='ajout_categorie',
                utilisateur=request.user.username,
                categorie=categorie,
                details=f"Ajout de la catégorie : {categorie.nom}"
            )
            messages.success(request, f"La catégorie '{categorie.nom}' a été ajoutée avec succès.")
            return redirect('admin_dashboard')
    else:
        form = CategorieForm()
    return render(request, 'archivage/ajouter_categorie.html', {'form': form})

@user_passes_test(is_admin)
def modifier_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            categorie = form.save()
            # Enregistrer dans l'historique
            Historique.objects.create(
                type_element='categorie',
                action='modification_categorie',
                utilisateur=request.user.username,
                categorie=categorie,
                details=f"Modification de la catégorie : {categorie.nom}"
            )
            messages.success(request, f"La catégorie '{categorie.nom}' a été modifiée avec succès.")
            return redirect('admin_dashboard')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'archivage/modifier_categorie.html', {'form': form})

@user_passes_test(is_admin)
def supprimer_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    nom_categorie = categorie.nom
    if request.method == 'POST':
        # Enregistrer dans l'historique avant la suppression
        Historique.objects.create(
            type_element='categorie',
            action='suppression_categorie',
            utilisateur=request.user.username,
            details=f"Suppression de la catégorie : {nom_categorie}"
        )
        categorie.delete()
        messages.success(request, f"La catégorie '{nom_categorie}' a été supprimée avec succès.")
        return redirect('admin_dashboard')
    return render(request, 'archivage/supprimer_categorie.html', {'categorie': categorie})

# @user_passes_test(is_admin)
def ajouter_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                document = form.save()
                
                # Enregistrer dans l'historique
                Historique.objects.create(
                    type_element='document',
                    action='ajout_document',
                    utilisateur=request.user.username,
                    document=document,
                    details=f"Ajout du document : {document.titre}"
                )
                
                messages.success(request, f"Le document '{document.titre}' a été ajouté avec succès.")
                return redirect('liste_documents_admin')
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de l'ajout du document : {str(e)}")
        else:
            # Afficher les erreurs de validation
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"Erreur dans le champ {field}: {error}")
    else:
        form = DocumentForm()
    
    return render(request, 'archivage/ajouter_document.html', {'form': form})

@user_passes_test(is_admin)
def modifier_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save()
            # Enregistrer dans l'historique
            Historique.objects.create(
                type_element='document',
                action='modification_document',
                utilisateur=request.user.username,
                document=document,
                details=f"Modification du document : {document.titre}"
            )
            messages.success(request, "Le document a été modifié avec succès.")
            return redirect('liste_documents_admin')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'archivage/modifier_document.html', {'form': form})

@user_passes_test(is_admin)
def supprimer_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    titre_document = document.titre
    if request.method == 'POST':
        # Enregistrer dans l'historique avant la suppression
        Historique.objects.create(
            type_element='document',
            action='suppression_document',
            utilisateur=request.user.username,
            details=f"Suppression du document : {titre_document}"
        )
        document.delete()
        messages.success(request, "Le document a été supprimé avec succès.")
        return redirect('liste_documents_admin')
    return render(request, 'archivage/supprimer_document.html', {'document': document})

@login_required
def liste_utilisateurs(request):
    query = request.GET.get('q', '')
    if query:
        utilisateurs = User.objects.filter(username__icontains=query)
    else:
        utilisateurs = User.objects.all()
    return render(request, 'archivage/liste_utilisateurs.html', {'utilisateurs': utilisateurs})

@login_required
def liste_historique(request):
    query = request.GET.get('q', '')
    type_filtre = request.GET.get('type', '')
    
    historique = Historique.objects.all()
    
    # Filtre par type
    if type_filtre:
        historique = historique.filter(type_element=type_filtre)
    
    # Recherche
    if query:
        historique = historique.filter(
            models.Q(action__icontains=query) |
            models.Q(details__icontains=query) |
            models.Q(utilisateur__icontains=query)
        )
    
    # Tri par date décroissante
    historique = historique.order_by('-date_action')
    
    return render(request, 'archivage/liste_historique.html', {
        'historique': historique,
        'type_filtre': type_filtre,
    })

@user_passes_test(is_admin)
def ajouter_utilisateur(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Enregistrer dans l'historique
            Historique.objects.create(
                type_element='utilisateur',
                action='ajout_utilisateur',
                utilisateur=request.user.username,
                details=f"Ajout de l'utilisateur : {user.username}"
            )
            messages.success(request, f"L'utilisateur {user.username} a été créé avec succès.")
            return redirect('liste_utilisateurs')  # Redirection vers la liste des utilisateurs
    else:
        form = CustomUserCreationForm()
    return render(request, 'archivage/ajouter_utilisateur.html', {'form': form})

@user_passes_test(is_admin)
def supprimer_utilisateur(request, user_id):
    user = get_object_or_404(User, id=user_id)
    username = user.username
    if request.method == 'POST':
        # Enregistrer dans l'historique avant la suppression
        Historique.objects.create(
            type_element='utilisateur',
            action='suppression_utilisateur',
            utilisateur=request.user.username,
            details=f"Suppression de l'utilisateur : {username}"
        )
        user.delete()
        messages.success(request, f"L'utilisateur {username} a été supprimé avec succès.")
        return redirect('liste_utilisateurs')
    return render(request, 'archivage/supprimer_utilisateur.html', {'user': user})

def documents(request):
    # Récupérer le paramètre de recherche
    query = request.GET.get('q', '')
    categorie_id = request.GET.get('categorie')
    visibilite = request.GET.get('visibilite')
    
    # Filtrer les documents
    if request.user.is_authenticated:
        # Les utilisateurs connectés peuvent voir tous les documents
        documents = Document.objects.all()
    else:
        # Les utilisateurs non connectés ne peuvent voir que les documents publics
        documents = Document.objects.filter(visibilite='publique')
    
    if query:
        documents = documents.filter(
            Q(titre__icontains=query) |
            Q(description__icontains=query) |
            Q(categorie__nom__icontains=query)
        )
    
    if categorie_id:
        documents = documents.filter(categorie_id=categorie_id)
        
    if visibilite:
        if not request.user.is_authenticated and visibilite == 'privee':
            messages.warning(request, "Vous devez être connecté pour voir les documents privés.")
            documents = documents.none()
        else:
            documents = documents.filter(visibilite=visibilite)

    # Récupérer toutes les catégories pour le filtre
    categories = Categorie.objects.all()
    
    context = {
        'documents': documents,
        'categories': categories,
        'query': query,
        'categorie_selectionnee': str(categorie_id) if categorie_id else '',
        'visibilite_selectionnee': visibilite,
        'peut_voir_prives': request.user.is_authenticated
    }
    
    return render(request, 'archivage/documents.html', context)

# @user_passes_test(is_admin)
def creer_categorie_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nom = data.get('nom')
            description = data.get('description', '')

            if not nom:
                return JsonResponse({'success': False, 'error': 'Le nom de la catégorie est requis.'})

            # Vérifier si une catégorie avec ce nom existe déjà
            if Categorie.objects.filter(nom=nom).exists():
                return JsonResponse({'success': False, 'error': 'Une catégorie avec ce nom existe déjà.'})

            # Créer la catégorie
            categorie = Categorie.objects.create(
                nom=nom,
                description=description
            )

            # Enregistrer dans l'historique
            Historique.objects.create(
                type_element='categorie',
                action='ajout_categorie',
                utilisateur=request.user.username,
                categorie=categorie,
                details=f"Ajout de la catégorie : {categorie.nom}"
            )

            messages.success(request, f"La catégorie '{categorie.nom}' a été ajoutée avec succès.")
            return JsonResponse({
                'success': True,
                'redirect': reverse('admin_dashboard'),
                'categorie': {
                    'id': categorie.id,
                    'nom': categorie.nom
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Données JSON invalides.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'})

def register(request):
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.password = make_password(form.cleaned_data['password1'])
            registration.save()
            messages.success(request, 'Votre demande d\'inscription a été envoyée. Un administrateur va la examiner.')
            return redirect('login')
    else:
        form = RegistrationRequestForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def pending_registrations(request):
    pending_requests = RegistrationRequest.objects.filter(is_approved=False, is_rejected=False)
    return render(request, 'archivage/pending_registrations.html', {
        'pending_requests': pending_requests
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_registration(request, request_id):
    reg_request = get_object_or_404(RegistrationRequest, id=request_id)
    if request.method == 'POST':
        if 'approve' in request.POST:
            # Créer un nouvel utilisateur désactivé
            user = User.objects.create(
                username=reg_request.username,
                email=reg_request.email,
                password=reg_request.password,  # Déjà hashé
                first_name=reg_request.first_name,
                last_name=reg_request.last_name,
                is_active=False  # L'utilisateur est créé mais désactivé
            )
            reg_request.is_approved = True
            reg_request.save()
            messages.success(request, f'L\'utilisateur {reg_request.username} a été créé. Vous pouvez maintenant l\'activer depuis la liste des utilisateurs.')
        elif 'reject' in request.POST:
            reg_request.is_rejected = True
            reg_request.admin_note = request.POST.get('admin_note', '')
            reg_request.save()
            messages.warning(request, f'La demande de {reg_request.username} a été rejetée.')
    return redirect('liste_utilisateurs')  # Rediriger vers la liste des utilisateurs au lieu de pending_registrations