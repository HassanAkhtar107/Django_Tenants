from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True

class Domain(DomainMixin):
    pass

# class User(AbstractUser):
#     pass

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username=f"{first_name}{last_name}".lower()
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser is_superuser=True.')
        return self.create_user(email, first_name, last_name, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=150, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10,  default='user')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'users'
    #     ordering = ['-created_at']