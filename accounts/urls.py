from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Connexion personnalisée
    path('login/', views.custom_login, name='login'),
    
    # Déconnexion
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    
    # Inscription
    path('register/', views.register, name='register'),
]