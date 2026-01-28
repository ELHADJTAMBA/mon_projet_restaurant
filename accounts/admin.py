from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Administration personnalisée pour le modèle User"""
    
    list_display = ('login', 'role', 'actif', 'date_creation', 'is_staff')
    list_filter = ('role', 'actif', 'is_staff', 'date_creation')
    search_fields = ('login',)
    ordering = ('-date_creation',)
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('login', 'password', 'role', 'actif')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_creation'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'role', 'password1', 'password2', 'actif', 'is_staff'),
        }),
    )
    
    readonly_fields = ('date_creation', 'last_login')
    filter_horizontal = ('groups', 'user_permissions')




