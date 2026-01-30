from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # ==================== ROUTES COMMUNES ====================
    path('', views.menu_list, name='menu_list'),
    path('api/plats/', views.plat_list_api, name='plat_list_api'),
    path('commande/<int:commande_id>/', views.detail_commande, name='detail_commande'),
    
    # ==================== ROUTES TABLE ====================
    path('panier/', views.panier_view, name='panier'),
    path('panier/ajouter/<int:plat_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/modifier/<int:item_id>/', views.modifier_panier_item, name='modifier_panier_item'),
    path('panier/supprimer/<int:item_id>/', views.supprimer_panier_item, name='supprimer_panier_item'),
    path('panier/vider/', views.vider_panier, name='vider_panier'),
    path('commander/', views.valider_commande, name='valider_commande'),
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
    
    # ==================== ROUTES CUISINIER ====================
    path('cuisinier/', views.tableau_bord_cuisinier, name='tableau_bord_cuisinier'),
    path('cuisinier/plats/', views.gestion_plats_cuisinier, name='gestion_plats_cuisinier'),
    path('cuisinier/plats/ajouter/', views.ajouter_plat, name='ajouter_plat'),
    path('cuisinier/plats/<int:plat_id>/modifier/', views.modifier_plat, name='modifier_plat'),
    path('cuisinier/plats/<int:plat_id>/disponibilite/', views.changer_disponibilite_plat, name='changer_disponibilite_plat'),
    path('cuisinier/commandes/<int:commande_id>/statut/', views.changer_statut_commande, name='changer_statut_commande'),
    
    # ==================== ROUTES COMPTABLE ====================
    path('comptable/', views.tableau_bord_comptable, name='tableau_bord_comptable'),
    path('comptable/paiements/', views.liste_paiements, name='liste_paiements'),
    path('comptable/depenses/', views.liste_depenses, name='liste_depenses'),
    path('comptable/depenses/ajouter/', views.ajouter_depense, name='ajouter_depense'),
    path('comptable/rapport/', views.rapport_financier, name='rapport_financier'),
]