from django.contrib import admin
from apps.users.models import User
from apps.users.models import Rol

admin.site.register(Rol)
admin.site.register(User)