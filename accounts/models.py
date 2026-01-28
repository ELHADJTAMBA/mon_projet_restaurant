from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    """Gestionnaire personnalisé pour le modèle User"""
    
    def create_user(self, login, password=None, role='Rtable'):
        """Créer et sauvegarder un utilisateur"""
        if not login:
            raise ValueError("Le login est obligatoire")
        
        user = self.model(login=login, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, login, password):
        """Créer et sauvegarder un super utilisateur"""
        user = self.create_user(
            login=login,
            password=password,
            role='Radmin'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé"""
    
    ROLE_CHOICES = [
        ('Rtable', 'Table'),
        ('Rservent', 'Serveur'),
        ('Rcuisinier', 'Cuisinier'),
        ('Rcomptable', 'Comptable'),
        ('Radmin', 'Administrateur'),
    ]
    
    login = models.CharField(max_length=30, unique=True, verbose_name='Identifiant')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='Rôle')
    actif = models.BooleanField(default=True, verbose_name='Actif')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.login} ({self.get_role_display()})"




