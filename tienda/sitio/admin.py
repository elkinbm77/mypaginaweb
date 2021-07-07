from django.contrib import admin
from .models import Articulo, Seccion, Producto, Categoria, Carrito

# Register your models here.
admin.site.register(Articulo)
admin.site.register(Seccion)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Carrito)