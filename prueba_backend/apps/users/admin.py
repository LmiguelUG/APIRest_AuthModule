from django.contrib import admin
from apps.users.models import User
from apps.users.models import Rol
from django.contrib.auth.models import Permission

admin.site.register(Rol)
admin.site.register(User)
admin.site.register(Permission)