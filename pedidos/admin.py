from django.contrib import admin
from .models import Producto, Categoria

admin.site.register(Categoria)
admin.site.register(Producto)