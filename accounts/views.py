from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import User


def register(request):
    """Vue d'inscription (optionnelle)"""
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