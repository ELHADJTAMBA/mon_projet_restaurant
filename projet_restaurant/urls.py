from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Redirection de la racine vers le menu
    path('', RedirectView.as_view(url='/menu/', permanent=False), name='home'),
    
    # Applications
    path('accounts/', include('accounts.urls')),
    path('menu/', include('menu.urls')),
    path('tables/', include('tables.urls')),
]

# Configuration pour servir les fichiers statiques et médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configuration de l'administration
admin.site.site_header = "RestauPro - Administration"
admin.site.site_title = "RestauPro Admin"
admin.site.index_title = "Gestion du restaurant"




