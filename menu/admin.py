from django.contrib import admin
from .models import Plat, Commande, CommandeItem, Panier, PanierItem, Paiement, Caisse, Depense


@admin.register(Plat)
class PlatAdmin(admin.ModelAdmin):
    """Administration pour les plats"""
    
    list_display = ('nom', 'categorie', 'prix', 'disponible', 'date_creation')
    list_filter = ('categorie', 'disponible', 'date_creation')
    search_fields = ('nom', 'description')
    list_editable = ('disponible',)
    ordering = ('categorie', 'nom')
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'description', 'categorie', 'prix')
        }),
        ('Médias', {
            'fields': ('image',)
        }),
        ('Disponibilité', {
            'fields': ('disponible',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('date_creation', 'date_modification')


class CommandeItemInline(admin.TabularInline):
    """Inline pour les articles de commande"""
    model = CommandeItem
    extra = 0
    readonly_fields = ('plat', 'quantite', 'prix_unitaire', 'total')
    can_delete = False
    
    def total(self, obj):
        return obj.total
    total.short_description = 'Total (GNF)'


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    """Administration pour les commandes"""
    
    list_display = ('id', 'table', 'montant_total', 'statut', 'date_commande', 'serveur')
    list_filter = ('statut', 'date_commande', 'table')
    search_fields = ('table__numero_table', 'serveur__login')
    list_editable = ('statut',)
    ordering = ('-date_commande',)
    inlines = [CommandeItemInline]
    
    fieldsets = (
        ('Informations de la commande', {
            'fields': ('table', 'montant_total', 'statut')
        }),
        ('Serveur', {
            'fields': ('serveur',)
        }),
        ('Date', {
            'fields': ('date_commande',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('date_commande', 'montant_total')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('table', 'serveur')


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    """Administration pour les paiements"""
    
    list_display = ('id', 'commande', 'montant', 'date_paiement')
    list_filter = ('date_paiement',)
    search_fields = ('commande__id', 'commande__table__numero_table')
    ordering = ('-date_paiement',)
    
    fieldsets = (
        ('Informations du paiement', {
            'fields': ('commande', 'montant')
        }),
        ('Date', {
            'fields': ('date_paiement',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('date_paiement',)


@admin.register(Caisse)
class CaisseAdmin(admin.ModelAdmin):
    """Administration pour la caisse"""
    
    list_display = ('id', 'solde_actuel', 'derniere_mise_a_jour')
    
    fieldsets = (
        ('Solde', {
            'fields': ('solde_actuel',)
        }),
        ('Dernière mise à jour', {
            'fields': ('derniere_mise_a_jour',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('derniere_mise_a_jour',)
    
    def has_add_permission(self, request):
        # Empêcher la création de plusieurs caisses
        try:
            return not Caisse.objects.exists()
        except:
            # Si la table n'existe pas, permettre la création
            return True
    
    def has_delete_permission(self, request, obj=None):
        # Empêcher la suppression de la caisse
        return False


@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    """Administration pour les dépenses"""
    
    list_display = ('motif', 'montant', 'date', 'enregistre_par')
    list_filter = ('date', 'enregistre_par')
    search_fields = ('motif',)
    ordering = ('-date',)
    
    fieldsets = (
        ('Informations de la dépense', {
            'fields': ('motif', 'montant')
        }),
        ('Enregistrement', {
            'fields': ('enregistre_par', 'date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('date',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('enregistre_par')