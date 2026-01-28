from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # Liste des plats (page principale)
    path('', views.menu_list, name='menu_list'),
    
    # API pour récupérer les plats
    path('api/plats/', views.plat_list_api, name='plat_list_api'),
    
    # Gestion du panier
    path('panier/', views.panier_view, name='panier'),
    path('panier/ajouter/<int:plat_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/modifier/<int:item_id>/', views.modifier_panier_item, name='modifier_panier_item'),
    path('panier/supprimer/<int:item_id>/', views.supprimer_panier_item, name='supprimer_panier_item'),
    path('panier/vider/', views.vider_panier, name='vider_panier'),
    
    # Validation de la commande
    path('commander/', views.valider_commande, name='valider_commande'),
    
    # Mes commandes
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
    path('commande/<int:commande_id>/', views.detail_commande, name='detail_commande'),
]