from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    # Dashboard administrateur
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
