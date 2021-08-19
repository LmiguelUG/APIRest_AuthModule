from django.db import models

# Modelo de Rol de usuario
class Rol(models.Model):
    id = models.AutoField(primary_key = True)
    rol = models.CharField('Rol', max_length=50,unique=True)
    
    def __str__(self):
        return self.rol