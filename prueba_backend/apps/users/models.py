from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Modelo de Rol de usuario
class Rol(models.Model):
    id = models.AutoField(primary_key = True)
    rol = models.CharField('Rol', max_length=50,unique=True)
    
    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.rol

# User manager model
class UserManager(BaseUserManager):
    def _create_user(self, username, email, name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, True, True, **extra_fields)

AUTH_PROVIDERS = {'facebook':'facebook','google':'google','email':'email'}

# User model
class User(AbstractBaseUser, PermissionsMixin):
    username  = models.CharField (max_length=255,unique=True)
    email     = models.EmailField('Correo Electronico',max_length=255,unique=True) 
    name      = models.CharField ('Nombre',max_length=255,blank=True, null=True)
    image     = models.ImageField('Imagen de Perfil',upload_to='perfil/',max_length=255,null=True,blank=True)
    last_name = models.CharField ('Apellido',max_length=255,blank=True, null=True)
    rol       = models.ManyToManyField(Rol)
    is_activate   = models.BooleanField(default=True)
    is_staff      = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default = AUTH_PROVIDERS.get('email'))
    objects       = UserManager()
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS = ['name','last_name','email']

    def natural_key(self):
        return (self.username)

    def __str__(self):
        return f'{self.name} {self.last_name}'


