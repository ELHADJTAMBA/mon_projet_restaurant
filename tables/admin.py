from django.contrib import admin
from .models import TableRestaurant

@admin.register(TableRestaurant)
class TableRestaurantAdmin(admin.ModelAdmin):
    """Administration pour les tables du restaurant"""
    
    list_display = ('numero_table', 'nombre_places', 'etat', 'utilisateur', 'date_creation')
    list_filter = ('etat', 'nombre_places', 'date_creation')
    search_fields = ('numero_table', 'utilisateur__login')
    list_editable = ('etat',)
    ordering = ('numero_table',)
    
    fieldsets = (
        ('Informations de la table', {
            'fields': ('numero_table', 'nombre_places', 'utilisateur')
        }),
        ('État actuel', {
            'fields': ('etat',)
        }),
        ('Dates', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('date_creation',)
    
    def get_queryset(self, request):
        """Optimiser la requête avec select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('utilisateur')




