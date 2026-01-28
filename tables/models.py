from django.db import models
from django.conf import settings

class TableRestaurant(models.Model):
    """Modèle représentant une table du restaurant"""
    
    ETAT_CHOICES = [
        ('libre', 'Libre'),
        ('attente', 'Commande en attente'),
        ('servie', 'Commande servie'),
        ('payee', 'Commande payée'),
    ]
    
    numero_table = models.CharField(max_length=10, unique=True, verbose_name='Numéro de table')
    nombre_places = models.PositiveIntegerField(default=4, verbose_name='Nombre de places')
    etat = models.CharField(
        max_length=10,
        choices=ETAT_CHOICES,
        default='libre',
        verbose_name='État'
    )
    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Rtable'},
        related_name='table_restaurant',
        verbose_name='Utilisateur'
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    
    class Meta:
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'
        ordering = ['numero_table']
    
    def __str__(self):
        return f"Table {self.numero_table} - {self.get_etat_display()}"




