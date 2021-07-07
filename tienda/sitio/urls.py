from django.urls import path, include
from . import views

app_name = "sitio"
urlpatterns = [
    path('', views.index, name="index"),
    #
    path('filtro_categorias/<int:categoria_id>', views.filtro_categorias, name="filtro_categorias"),
    path('filtro_productos', views.filtro_productos, name="filtro_productos"),    
    #   
    path('<int:producto_id>', views.producto, name="producto"),
    #
    path('producto_alta', views.producto_alta, name="producto_alta"),
    #
    path('producto_editar/<int:producto_id>', views.producto_editar, name="producto_editar"),
    path('producto_eliminar/<int:producto_id>', views.producto_eliminar, name="producto_eliminar"),
    #
    path('carrito/<int:producto_id>', views.carrito, name="carrito"),
    path('consultar_carrito', views.consultar_carrito, name="consultar_carrito"),
    #
    #path('carrito_quitar/<int:producto_id', views.carrito_quitar, name="carrito_quitar"),

    path('carrito_quitar', views.carrito_quitar, name="carrito_quitar"),
    path('carrito_eliminar', views.carrito_eliminar, name="carrito_eliminar"),
    #
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('envia_correo', views.envia_correo, name="envia_correo"),
 
]