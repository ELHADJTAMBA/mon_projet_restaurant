from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .models import TableRestaurant
from menu.models import Commande, Paiement, Caisse
from accounts.decorators import serveur_only


@login_required
@serveur_only
def serveur_dashboard(request):
    """Dashboard professionnel pour le rôle serveur"""
    tables = TableRestaurant.objects.select_related('utilisateur').all()
    
    # Statistiques détaillées
    stats = {
        'total': tables.count(),
        'libres': tables.filter(etat='libre').count(),
        'attente': tables.filter(etat='attente').count(),
        'servies': tables.filter(etat='servie').count(),
        'payees': tables.filter(etat='payee').count(),
    }
    
    # Tables nécessitant une attention
    tables_en_attente = tables.filter(etat='attente')
    tables_a_payer = tables.filter(etat='servie')
    
    context = {
        'tables': tables,
        'stats': stats,
        'tables_en_attente': tables_en_attente,
        'tables_a_payer': tables_a_payer,
    }
    
    return render(request, 'tables/serveur_dashboard.html', context)


@login_required
@serveur_only
def liste_tables(request):
    """Liste de toutes les tables du restaurant"""
    tables = TableRestaurant.objects.select_related('utilisateur').all()
    
    # Statistiques
    stats = {
        'total': tables.count(),
        'libres': tables.filter(etat='libre').count(),
        'attente': tables.filter(etat='attente').count(),
        'servies': tables.filter(etat='servie').count(),
        'payees': tables.filter(etat='payee').count(),
    }
    
    context = {
        'tables': tables,
        'stats': stats,
    }
    
    return render(request, 'tables/liste_tables.html', context)


@login_required
@serveur_only
def detail_table(request, table_id):
    """Détail d'une table et ses commandes"""
    table = get_object_or_404(TableRestaurant, id=table_id)
    
    # Récupérer les commandes de la table
    commandes = table.commandes.order_by('-date_commande')
    
    # Commande en cours (non payée)
    commande_en_cours = commandes.filter(statut__in=['en_attente', 'en_preparation', 'prete', 'servie']).first()
    
    context = {
        'table': table,
        'commandes': commandes,
        'commande_en_cours': commande_en_cours,
    }
    
    return render(request, 'tables/detail_table.html', context)


@login_required
@serveur_only
@transaction.atomic
def changer_etat_table(request, table_id):
    """Changer l'état d'une table et/ou valider le paiement"""
    if request.method == 'POST':
        table = get_object_or_404(TableRestaurant, id=table_id)
        action = request.POST.get('action')
        
        try:
            if action == 'marquer_servie':
                # Marquer la commande comme servie
                commande = table.commandes.filter(statut__in=['en_attente', 'en_preparation', 'prete']).first()
                if commande:
                    commande.statut = 'servie'
                    commande.serveur = request.user
                    commande.save()
                    
                    table.etat = 'servie'
                    table.save()
                    
                    messages.success(request, f"Table {table.numero_table} marquée comme servie.")
                else:
                    messages.error(request, "Aucune commande à servir pour cette table.")
            
            elif action == 'valider_paiement':
                # Valider le paiement
                commande = table.commandes.filter(statut='servie').first()
                if commande:
                    # Créer le paiement
                    paiement = Paiement.objects.create(
                        commande=commande,
                        montant=commande.montant_total
                    )
                    
                    # Mettre à jour le statut de la commande
                    commande.statut = 'payee'
                    commande.save()
                    
                    # Mettre à jour l'état de la table
                    table.etat = 'libre'
                    table.save()
                    
                    # Mettre à jour la caisse
                    caisse, created = Caisse.objects.get_or_create(id=1)
                    caisse.solde_actuel += commande.montant_total
                    caisse.save()
                    
                    messages.success(request, f"Paiement validé pour la table {table.numero_table}. Montant : {commande.montant_total} GNF")
                else:
                    messages.error(request, "Aucune commande à payer pour cette table.")
            
            else:
                messages.error(request, "Action non reconnue.")
            
            return redirect('tables:detail_table', table_id=table_id)
            
        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")
            return redirect('tables:detail_table', table_id=table_id)
    
    return redirect('tables:liste_tables')