from django.urls import path
from . import views

app_name = 'tables'

urlpatterns = [
    # Liste des tables (pour serveurs/admin)
    path('', views.liste_tables, name='liste_tables'),
    
    # Détail d'une table
    path('<int:table_id>/', views.detail_table, name='detail_table'),
    
    # Changer l'état d'une table
    path('<int:table_id>/changer-etat/', views.changer_etat_table, name='changer_etat_table'),
]




