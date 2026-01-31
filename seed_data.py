# -*- coding: utf-8 -*-
"""
Script pour generer des donnees de test pour RestauPro
Executer avec : python manage.py shell < seed_data_fixed.py
OU : Get-Content seed_data_fixed.py -Encoding UTF8 | python manage.py shell
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_restaurant.settings')
django.setup()

from decimal import Decimal
from accounts.models import User
from tables.models import TableRestaurant
from menu.models import Plat, Caisse

print("=" * 60)
print("  DEBUT DE LA GENERATION DES DONNEES DE TEST")
print("=" * 60)

# 1. Creer des utilisateurs
print("\n[1/4] Creation des utilisateurs...")

# Admin
admin, created = User.objects.get_or_create(
    login='admin',
    defaults={
        'role': 'Radmin',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print("  OK Admin cree : admin / admin123")
else:
    print("  INFO Admin existe deja")

# Serveurs
serveurs_data = [
    ('SERV001', 'serveur123'),
    ('SERV002', 'serveur123'),
]

for login, password in serveurs_data:
    serveur, created = User.objects.get_or_create(
        login=login,
        defaults={'role': 'Rservent'}
    )
    if created:
        serveur.set_password(password)
        serveur.save()
        print(f"  OK Serveur cree : {login} / {password}")

# Cuisinier
cuisinier, created = User.objects.get_or_create(
    login='CUISI001',
    defaults={'role': 'Rcuisinier'}
)
if created:
    cuisinier.set_password('cuisinier123')
    cuisinier.save()
    print("  OK Cuisinier cree : CUISI001 / cuisinier123")

# Comptable
comptable, created = User.objects.get_or_create(
    login='COMPT001',
    defaults={'role': 'Rcomptable'}
)
if created:
    comptable.set_password('comptable123')
    comptable.save()
    print("  OK Comptable cree : COMPT001 / comptable123")

# Tables
print("\n[2/4] Creation des tables...")
tables_data = [
    ('TABLE001', 'table001', 4),
    ('TABLE002', 'table002', 4),
    ('TABLE003', 'table003', 2),
    ('TABLE004', 'table004', 6),
    ('TABLE005', 'table005', 4),
    ('TABLE006', 'table006', 8),
]

for login, password, places in tables_data:
    user_table, user_created = User.objects.get_or_create(
        login=login,
        defaults={'role': 'Rtable'}
    )
    if user_created:
        user_table.set_password(password)
        user_table.save()
        
        table, table_created = TableRestaurant.objects.get_or_create(
            numero_table=login.replace('TABLE', ''),
            defaults={
                'utilisateur': user_table,
                'nombre_places': places
            }
        )
        print(f"  OK Table creee : {login} / {password} ({places} places)")

# 2. Creer des plats
print("\n[3/4] Creation des plats...")

plats_data = [
    # Entrees
    ('Salade Cesar', 'Salade romaine, poulet grille, parmesan, croutons', Decimal('15000'), 'ENTREE'),
    ('Soupe du jour', 'Soupe fraiche preparee quotidiennement', Decimal('8000'), 'ENTREE'),
    ('Nems au poulet', '6 nems croustillants avec sauce', Decimal('12000'), 'ENTREE'),
    ('Bruschetta', 'Pain grille, tomates fraiches, basilic', Decimal('10000'), 'ENTREE'),
    
    # Plats principaux
    ('Riz au gras', 'Riz cuisine a la viande et aux legumes', Decimal('25000'), 'PLAT'),
    ('Poulet braise', 'Poulet marine et grille avec frites', Decimal('30000'), 'PLAT'),
    ('Poisson grille', 'Poisson frais du jour avec riz', Decimal('35000'), 'PLAT'),
    ('Spaghetti bolognaise', 'Pates fraiches, sauce tomate, viande hachee', Decimal('28000'), 'PLAT'),
    ('Pizza Margherita', 'Tomate, mozzarella, basilic', Decimal('32000'), 'PLAT'),
    ('Steak frites', 'Boeuf grille avec frites maison', Decimal('40000'), 'PLAT'),
    ('Riz sauce arachide', 'Riz avec sauce aux arachides et viande', Decimal('25000'), 'PLAT'),
    ('Couscous poulet', 'Couscous, poulet, legumes', Decimal('35000'), 'PLAT'),
    
    # Desserts
    ('Tarte aux pommes', 'Tarte maison avec glace vanille', Decimal('12000'), 'DESSERT'),
    ('Tiramisu', 'Dessert italien au cafe', Decimal('15000'), 'DESSERT'),
    ('Salade de fruits', 'Fruits frais de saison', Decimal('10000'), 'DESSERT'),
    ('Creme brulee', 'Dessert francais cremeux', Decimal('14000'), 'DESSERT'),
    
    # Boissons
    ('Coca-Cola', 'Soda 33cl', Decimal('3000'), 'BOISSON'),
    ('Fanta', 'Soda orange 33cl', Decimal('3000'), 'BOISSON'),
    ('Eau minerale', 'Bouteille 50cl', Decimal('2000'), 'BOISSON'),
    ('Jus d\'orange', 'Jus frais presse', Decimal('5000'), 'BOISSON'),
    ('Cafe', 'Cafe expresso', Decimal('4000'), 'BOISSON'),
    ('The', 'The chaud ou glace', Decimal('3000'), 'BOISSON'),
]

plats_crees = 0
for nom, description, prix, categorie in plats_data:
    plat, created = Plat.objects.get_or_create(
        nom=nom,
        defaults={
            'description': description,
            'prix': prix,
            'categorie': categorie,
            'disponible': True
        }
    )
    if created:
        plats_crees += 1

print(f"  OK {plats_crees} plats crees")

# 3. Creer la caisse
print("\n[4/4] Creation de la caisse...")
caisse, created = Caisse.objects.get_or_create(
    id=1,
    defaults={'solde_actuel': Decimal('0.00')}
)
if created:
    print("  OK Caisse creee avec un solde initial de 0 GNF")
else:
    print(f"  INFO Caisse existe deja - Solde actuel : {caisse.solde_actuel} GNF")

print("\n" + "=" * 60)
print("  GENERATION DES DONNEES TERMINEE AVEC SUCCES !")
print("=" * 60)
print("\nRESUME DES COMPTES CREES :")
print("-" * 60)
print("Admin:")
print("  Login: admin          | Password: admin123")
print("\nServeurs:")
print("  Login: SERV001        | Password: serveur123")
print("  Login: SERV002        | Password: serveur123")
print("\nCuisinier:")
print("  Login: CUISI001       | Password: cuisinier123")
print("\nComptable:")
print("  Login: COMPT001       | Password: comptable123")
print("\nTables:")
for i in range(1, 7):
    print(f"  Login: TABLE{i:03d}       | Password: table{i:03d}")
print("-" * 60)
print("\nPour vous connecter, allez sur:")
print("  http://127.0.0.1:8000/accounts/login/")
print("=" * 60)




