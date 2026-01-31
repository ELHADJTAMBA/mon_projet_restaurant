from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import User
from tables.models import TableRestaurant
from menu.models import Plat, Caisse, Commande
from django.db.models import Count

@staff_member_required
def admin_dashboard(request):
    """Dashboard pour les super administrateurs"""
    
    # Statistiques globales
    total_users = User.objects.count()
    total_tables = TableRestaurant.objects.count()
    total_plats = Plat.objects.count()
    
    # Solde de la caisse
    try:
        caisse = Caisse.objects.get(id=1)
        caisse_solde = caisse.solde_actuel
    except:
        caisse_solde = 0
    
    # Derniere commande
    last_commande = Commande.objects.order_by('-date_commande').first()
    last_commande_id = last_commande.id if last_commande else 0
    
    context = {
        'total_users': total_users,
        'total_tables': total_tables,
        'total_plats': total_plats,
        'caisse_solde': caisse_solde,
        'last_commande_id': last_commande_id,
    }
    
    return render(request, 'admin/admin_dashboard.html', context)
