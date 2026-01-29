from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q, Sum, Count
from decimal import Decimal

from .models import Plat, Panier, PanierItem, Commande, CommandeItem, Paiement
from tables.models import TableRestaurant
from accounts.decorators import table_only, serveur_only


@login_required
def menu_list(request):
    """Liste des plats disponibles"""
    categorie = request.GET.get('categorie', '')
    recherche = request.GET.get('q', '')
    
    plats = Plat.objects.filter(disponible=True)
    
    if categorie:
        plats = plats.filter(categorie=categorie)
    
    if recherche:
        plats = plats.filter(
            Q(nom__icontains=recherche) | Q(description__icontains=recherche)
        )
    
    # Regrouper par catégorie
    plats_par_categorie = {}
    for categorie_code, categorie_nom in Plat.CATEGORIES:
        plats_categorie = plats.filter(categorie=categorie_code)
        if plats_categorie.exists():
            plats_par_categorie[categorie_nom] = plats_categorie
    
    # Récupérer le panier actif pour l'utilisateur table
    panier = None
    panier_count = 0
    if request.user.role == 'Rtable':
        try:
            table = request.user.table_restaurant
            panier = Panier.objects.filter(table=table, actif=True).first()
            if panier:
                panier_count = panier.items.count()
        except:
            pass
    
    context = {
        'plats_par_categorie': plats_par_categorie,
        'categories': Plat.CATEGORIES,
        'panier_count': panier_count,
    }
    
    return render(request, 'menu/menu_list.html', context)


@login_required
def plat_list_api(request):
    """API pour récupérer les plats (format JSON)"""
    plats = Plat.objects.filter(disponible=True).values(
        'id', 'nom', 'description', 'prix', 'categorie', 'image'
    )
    return JsonResponse(list(plats), safe=False)


@login_required
@table_only
def panier_view(request):
    """Afficher le panier"""
    try:
        table = request.user.table_restaurant
        panier = Panier.objects.filter(table=table, actif=True).first()
        
        if not panier:
            panier = Panier.objects.create(table=table)
        
        items = panier.items.select_related('plat').all()
        total = panier.total
        
        context = {
            'panier': panier,
            'items': items,
            'total': total,
        }
        
        return render(request, 'menu/panier.html', context)
    except:
        messages.error(request, "Erreur lors de l'accès au panier.")
        return redirect('menu:menu_list')


@login_required
@table_only
def ajouter_au_panier(request, plat_id):
    """Ajouter un plat au panier"""
    if request.method == 'POST':
        try:
            plat = get_object_or_404(Plat, id=plat_id, disponible=True)
            table = request.user.table_restaurant
            
            # Récupérer ou créer le panier actif
            panier, created = Panier.objects.get_or_create(
                table=table,
                actif=True
            )
            
            # Récupérer la quantité
            quantite = int(request.POST.get('quantite', 1))
            
            # Validation de la quantité
            if quantite < 1 or quantite > 10:
                messages.error(request, "La quantité doit être entre 1 et 10.")
                return redirect('menu:menu_list')
            
            # Vérifier si le plat est déjà dans le panier
            item, item_created = PanierItem.objects.get_or_create(
                panier=panier,
                plat=plat,
                defaults={
                    'quantite': quantite,
                    'prix_unitaire': plat.prix
                }
            )
            
            if not item_created:
                # Mettre à jour la quantité
                nouvelle_quantite = item.quantite + quantite
                if nouvelle_quantite > 10:
                    messages.error(request, "Vous ne pouvez pas commander plus de 10 unités d'un même plat.")
                    return redirect('menu:panier')
                
                item.quantite = nouvelle_quantite
                item.save()
                messages.success(request, f"{plat.nom} - quantité mise à jour dans le panier.")
            else:
                messages.success(request, f"{plat.nom} ajouté au panier.")
            
            return redirect('menu:panier')
            
        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout au panier : {str(e)}")
            return redirect('menu:menu_list')
    
    return redirect('menu:menu_list')


@login_required
@table_only
def modifier_panier_item(request, item_id):
    """Modifier la quantité d'un article dans le panier"""
    if request.method == 'POST':
        try:
            table = request.user.table_restaurant
            panier = get_object_or_404(Panier, table=table, actif=True)
            item = get_object_or_404(PanierItem, id=item_id, panier=panier)
            
            quantite = int(request.POST.get('quantite', 1))
            
            if quantite < 1 or quantite > 10:
                messages.error(request, "La quantité doit être entre 1 et 10.")
                return redirect('menu:panier')
            
            item.quantite = quantite
            item.save()
            
            messages.success(request, "Quantité mise à jour.")
            return redirect('menu:panier')
            
        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")
            return redirect('menu:panier')
    
    return redirect('menu:panier')


@login_required
@table_only
def supprimer_panier_item(request, item_id):
    """Supprimer un article du panier"""
    try:
        table = request.user.table_restaurant
        panier = get_object_or_404(Panier, table=table, actif=True)
        item = get_object_or_404(PanierItem, id=item_id, panier=panier)
        
        item.delete()
        messages.success(request, "Article supprimé du panier.")
        
    except Exception as e:
        messages.error(request, f"Erreur : {str(e)}")
    
    return redirect('menu:panier')


@login_required
@table_only
def vider_panier(request):
    """Vider le panier"""
    try:
        table = request.user.table_restaurant
        panier = get_object_or_404(Panier, table=table, actif=True)
        
        panier.items.all().delete()
        messages.success(request, "Panier vidé.")
        
    except Exception as e:
        messages.error(request, f"Erreur : {str(e)}")
    
    return redirect('menu:panier')


@login_required
@table_only
@transaction.atomic
def valider_commande(request):
    """Valider le panier et créer une commande"""
    if request.method == 'POST':
        try:
            table = request.user.table_restaurant
            panier = get_object_or_404(Panier, table=table, actif=True)
            
            # Vérifier que le panier n'est pas vide
            if not panier.items.exists():
                messages.error(request, "Votre panier est vide.")
                return redirect('menu:panier')
            
            # Calculer le montant total
            montant_total = panier.total
            
            # Créer la commande
            commande = Commande.objects.create(
                table=table,
                montant_total=montant_total,
                statut='en_attente'
            )
            
            # Créer les items de la commande
            for item in panier.items.all():
                CommandeItem.objects.create(
                    commande=commande,
                    plat=item.plat,
                    quantite=item.quantite,
                    prix_unitaire=item.prix_unitaire
                )
            
            # Désactiver le panier
            panier.actif = False
            panier.save()
            
            # Mettre à jour l'état de la table
            table.etat = 'attente'
            table.save()
            
            messages.success(request, f"Commande #{commande.id} créée avec succès ! Montant total : {montant_total} GNF")
            return redirect('menu:mes_commandes')
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la validation de la commande : {str(e)}")
            return redirect('menu:panier')
    
    return redirect('menu:panier')


@login_required
@table_only
def mes_commandes(request):
    """Liste des commandes de la table"""
    try:
        table = request.user.table_restaurant
        commandes = Commande.objects.filter(table=table).order_by('-date_commande')
        
        context = {
            'commandes': commandes,
        }
        
        return render(request, 'menu/mes_commandes.html', context)
    except:
        messages.error(request, "Erreur lors de la récupération des commandes.")
        return redirect('menu:menu_list')


@login_required
def detail_commande(request, commande_id):
    """Détail d'une commande"""
    commande = get_object_or_404(Commande, id=commande_id)
    
    # Vérifier les permissions
    if request.user.role == 'Rtable':
        if commande.table != request.user.table_restaurant:
            messages.error(request, "Vous n'avez pas accès à cette commande.")
            return redirect('menu:mes_commandes')
    elif request.user.role not in ['Rservent', 'Radmin', 'Rcomptable']:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('menu:menu_list')
    
    items = commande.items.select_related('plat').all()
    
    context = {
        'commande': commande,
        'items': items,
    }
    
    return render(request, 'menu/detail_commande.html', context)