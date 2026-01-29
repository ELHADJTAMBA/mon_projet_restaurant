"""
Script pour générer des données de test pour RestauPro
Exécuter avec : python manage.py shell < seed_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_restaurant.settings')
django.setup()

from decimal import Decimal
from accounts.models import User
from tables.models import TableRestaurant
from menu.models import Plat, Caisse

print("🚀 Début de la génération des données de test...")

# 1. Créer des utilisateurs
print("\n👥 Création des utilisateurs...")

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
    print("✅ Admin créé : admin / admin123")
else:
    print("ℹ️  Admin existe déjà")

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
        print(f"✅ Serveur créé : {login} / {password}")

# Cuisinier
cuisinier, created = User.objects.get_or_create(
    login='CUISI001',
    defaults={'role': 'Rcuisinier'}
)
if created:
    cuisinier.set_password('cuisinier123')
    cuisinier.save()
    print("✅ Cuisinier créé : CUISI001 / cuisinier123")

# Comptable
comptable, created = User.objects.get_or_create(
    login='COMPT001',
    defaults={'role': 'Rcomptable'}
)
if created:
    comptable.set_password('comptable123')
    comptable.save()
    print("✅ Comptable créé : COMPT001 / comptable123")

# Tables
print("\n🪑 Création des tables...")
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
        print(f"✅ Table créée : {login} / {password} ({places} places)")

# 2. Créer des plats
print("\n🍽️  Création des plats...")

plats_data = [
    # Entrées
    ('Salade César', 'Salade romaine, poulet grillé, parmesan, croûtons', Decimal('15000'), 'ENTREE'),
    ('Soupe du jour', 'Soupe fraîche préparée quotidiennement', Decimal('8000'), 'ENTREE'),
    ('Nems au poulet', '6 nems croustillants avec sauce', Decimal('12000'), 'ENTREE'),
    ('Bruschetta', 'Pain grillé, tomates fraîches, basilic', Decimal('10000'), 'ENTREE'),
    
    # Plats principaux
    ('Riz au gras', 'Riz cuisiné à la viande et aux légumes', Decimal('25000'), 'PLAT'),
    ('Poulet braisé', 'Poulet mariné et grillé avec frites', Decimal('30000'), 'PLAT'),
    ('Poisson grillé', 'Poisson frais du jour avec riz', Decimal('35000'), 'PLAT'),
    ('Spaghetti bolognaise', 'Pâtes fraîches, sauce tomate, viande hachée', Decimal('28000'), 'PLAT'),
    ('Pizza Margherita', 'Tomate, mozzarella, basilic', Decimal('32000'), 'PLAT'),
    ('Steak frites', 'Bœuf grillé avec frites maison', Decimal('40000'), 'PLAT'),
    ('Riz sauce arachide', 'Riz avec sauce aux arachides et viande', Decimal('25000'), 'PLAT'),
    ('Couscous poulet', 'Couscous, poulet, légumes', Decimal('35000'), 'PLAT'),
    
    # Desserts
    ('Tarte aux pommes', 'Tarte maison avec glace vanille', Decimal('12000'), 'DESSERT'),
    ('Tiramisu', 'Dessert italien au café', Decimal('15000'), 'DESSERT'),
    ('Salade de fruits', 'Fruits frais de saison', Decimal('10000'), 'DESSERT'),
    ('Crème brûlée', 'Dessert français crémeux', Decimal('14000'), 'DESSERT'),
    
    # Boissons
    ('Coca-Cola', 'Soda 33cl', Decimal('3000'), 'BOISSON'),
    ('Fanta', 'Soda orange 33cl', Decimal('3000'), 'BOISSON'),
    ('Eau minérale', 'Bouteille 50cl', Decimal('2000'), 'BOISSON'),
    ('Jus d\'orange', 'Jus frais pressé', Decimal('5000'), 'BOISSON'),
    ('Café', 'Café expresso', Decimal('4000'), 'BOISSON'),
    ('Thé', 'Thé chaud ou glacé', Decimal('3000'), 'BOISSON'),
]

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
        print(f"✅ Plat créé : {nom} - {prix} GNF")

# 3. Créer la caisse
print("\n💰 Création de la caisse...")
caisse, created = Caisse.objects.get_or_create(
    id=1,
    defaults={'solde_actuel': Decimal('0.00')}
)
if created:
    print("✅ Caisse créée avec un solde initial de 0 GNF")
else:
    print(f"ℹ️  Caisse existe déjà - Solde actuel : {caisse.solde_actuel} GNF")

print("\n✨ Génération des données terminée avec succès!")
print("\n📝 Résumé des comptes créés :")
print("=" * 50)
print("Admin:")
print("  Login: admin")
print("  Password: admin123")
print("\nServeurs:")
print("  Login: SERV001 | Password: serveur123")
print("  Login: SERV002 | Password: serveur123")
print("\nCuisinier:")
print("  Login: CUISI001 | Password: cuisinier123")
print("\nComptable:")
print("  Login: COMPT001 | Password: comptable123")
print("\nTables:")
for i in range(1, 7):
    print(f"  Login: TABLE{i:03d} | Password: table{i:03d}")
print("=" * 50)