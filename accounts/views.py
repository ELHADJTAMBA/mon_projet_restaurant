from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import User


def custom_login(request):
    """Vue de connexion personnalisée pour gérer le champ 'login'"""
    if request.user.is_authenticated:
        # Rediriger selon le rôle
        if request.user.is_superuser:
            return redirect('/admin/')
        elif request.user.role == 'Rtable':
            return redirect('menu:menu_list')
        elif request.user.role in ['Rservent', 'Radmin']:
            return redirect('tables:serveur_dashboard')
        elif request.user.role == 'Rcuisinier':
            return redirect('menu:tableau_bord_cuisinier')
        elif request.user.role == 'Rcomptable':
            return redirect('menu:tableau_bord_comptable')
        else:
            return redirect('menu:menu_list')
    
    if request.method == 'POST':
        login_user = request.POST.get('username')  # Le template envoie 'username'
        password = request.POST.get('password')
        
        # Validation
        if not login_user or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'accounts/login.html')
        
        # Authentification avec le champ 'login'
        user = authenticate(request, username=login_user, password=password)
        
        if user is not None:
            if user.actif:
                login(request, user)
                messages.success(request, f"Bienvenue {user.login} !")
                
                # Redirection selon le rôle
                if user.is_superuser:
                    return redirect('/admin/')
                elif user.role == 'Rtable':
                    return redirect('menu:menu_list')
                elif user.role in ['Rservent', 'Radmin']:
                    return redirect('tables:serveur_dashboard')
                elif user.role == 'Rcuisinier':
                    return redirect('menu:tableau_bord_cuisinier')
                elif user.role == 'Rcomptable':
                    return redirect('menu:tableau_bord_comptable')
                else:
                    return redirect('menu:menu_list')
            else:
                messages.error(request, "Votre compte est désactivé.")
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")
    
    return render(request, 'accounts/login.html')


def register(request):
    """Vue d'inscription"""
    if request.method == 'POST':
        login_user = request.POST.get('login')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        role = request.POST.get('role', 'Rtable')
        
        # Validations
        if not login_user or not password:
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, 'accounts/register.html')
        
        if len(login_user) < 6:
            messages.error(request, "Le login doit contenir au moins 6 caractères.")
            return render(request, 'accounts/register.html')
        
        if password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(login=login_user).exists():
            messages.error(request, "Ce login est déjà utilisé.")
            return render(request, 'accounts/register.html')
        
        # Créer l'utilisateur
        try:
            user = User.objects.create_user(
                login=login_user,
                password=password,
                role=role
            )
            messages.success(request, "Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
            return redirect('accounts:login')
        except Exception as e:
            messages.error(request, f"Erreur lors de la création du compte : {str(e)}")
    
    return render(request, 'accounts/register.html')