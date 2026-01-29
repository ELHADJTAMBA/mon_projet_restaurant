from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """
    Décorateur pour restreindre l'accès aux vues en fonction du rôle de l'utilisateur.
    
    Usage:
        @role_required('Rtable', 'Radmin')
        def ma_vue(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Vous devez être connecté pour accéder à cette page.")
                return redirect('accounts:login')
            
            if request.user.role not in roles:
                messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
                raise PermissionDenied
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def table_only(view_func):
    """Décorateur pour les vues accessibles uniquement aux tables"""
    return role_required('Rtable')(view_func)


def serveur_only(view_func):
    """Décorateur pour les vues accessibles uniquement aux serveurs"""
    return role_required('Rservent', 'Radmin')(view_func)


def cuisinier_only(view_func):
    """Décorateur pour les vues accessibles uniquement aux cuisiniers"""
    return role_required('Rcuisinier', 'Radmin')(view_func)


def comptable_only(view_func):
    """Décorateur pour les vues accessibles uniquement aux comptables"""
    return role_required('Rcomptable', 'Radmin')(view_func)


def admin_only(view_func):
    """Décorateur pour les vues accessibles uniquement aux administrateurs"""
    return role_required('Radmin')(view_func)