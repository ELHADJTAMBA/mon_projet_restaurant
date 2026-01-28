import os
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

def plat_image_path(instance, filename):
    """Générer le chemin de stockage des images de plats"""
    ext = filename.split('.')[-1]
    filename = f"{instance.nom.lower().replace(' ', '_')}.{ext}"
    return os.path.join('plats', filename)


class Plat(models.Model):
    """Modèle représentant un plat du menu"""
    
    CATEGORIES = [
        ('ENTREE', 'Entrée'),
        ('PLAT', 'Plat principal'),
        ('DESSERT', 'Dessert'),
        ('BOISSON', 'Boisson'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name='Nom du plat')
    description = models.TextField(blank=True, verbose_name='Description')
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Prix (GNF)'
    )
    categorie = models.CharField(max_length=10, choices=CATEGORIES, verbose_name='Catégorie')
    disponible = models.BooleanField(default=True, verbose_name='Disponible')
    image = models.ImageField(upload_to=plat_image_path, blank=True, null=True, verbose_name='Image')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='Date de modification')
    
    class Meta:
        verbose_name = 'Plat'
        verbose_name_plural = 'Plats'
        ordering = ['categorie', 'nom']
    
    def __str__(self):
        return f"{self.nom} - {self.prix} GNF"


class Commande(models.Model):
    """Modèle représentant une commande"""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_preparation', 'En préparation'),
        ('prete', 'Prête à servir'),
        ('servie', 'Servie'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée'),
    ]
    
    table = models.ForeignKey(
        'tables.TableRestaurant',
        on_delete=models.PROTECT,
        related_name='commandes',
        verbose_name='Table'
    )
    date_commande = models.DateTimeField(auto_now_add=True, verbose_name='Date de commande')
    montant_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Montant total (GNF)'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente',
        verbose_name='Statut'
    )
    serveur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commandes_servies',
        limit_choices_to={'role__in': ['Rservent', 'Radmin']},
        verbose_name='Serveur'
    )
    
    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-date_commande']
    
    def __str__(self):
        return f"Commande #{self.id} - Table {self.table.numero_table} - {self.montant_total} GNF"


class CommandeItem(models.Model):
    """Modèle représentant un article dans une commande"""
    
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Commande'
    )
    plat = models.ForeignKey(
        Plat,
        on_delete=models.PROTECT,
        verbose_name='Plat'
    )
    quantite = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantité'
    )
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Prix unitaire (GNF)'
    )
    
    class Meta:
        verbose_name = 'Article de commande'
        verbose_name_plural = 'Articles de commande'
    
    def __str__(self):
        return f"{self.quantite}x {self.plat.nom}"
    
    @property
    def total(self):
        """Calculer le total de l'article"""
        return self.quantite * self.prix_unitaire


class Panier(models.Model):
    """Modèle représentant un panier temporaire"""
    
    table = models.ForeignKey(
        'tables.TableRestaurant',
        on_delete=models.CASCADE,
        related_name='paniers',
        verbose_name='Table'
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    actif = models.BooleanField(default=True, verbose_name='Actif')
    
    class Meta:
        verbose_name = 'Panier'
        verbose_name_plural = 'Paniers'
    
    def __str__(self):
        return f"Panier - Table {self.table.numero_table}"
    
    @property
    def total(self):
        """Calculer le montant total du panier"""
        return sum(item.total for item in self.items.all())


class PanierItem(models.Model):
    """Modèle représentant un article dans le panier"""
    
    panier = models.ForeignKey(
        Panier,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Panier'
    )
    plat = models.ForeignKey(
        Plat,
        on_delete=models.PROTECT,
        verbose_name='Plat'
    )
    quantite = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name='Quantité'
    )
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Prix unitaire (GNF)'
    )
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'ajout')
    
    class Meta:
        verbose_name = 'Article du panier'
        verbose_name_plural = 'Articles du panier'
        unique_together = ['panier', 'plat']
    
    def __str__(self):
        return f"{self.quantite}x {self.plat.nom}"
    
    @property
    def total(self):
        """Calculer le total de l'article"""
        return self.quantite * self.prix_unitaire




