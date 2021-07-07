from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

""""""
class Seccion(models.Model):
    descripcion = models.CharField(max_length=64, null=False)

    def __str__(self):
        return f"{self.descripcion}"

class Articulo(models.Model):
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name="clasificacion_seccion")
    fecha_publicacion = models.DateField(null= False)
    titulo = models.CharField(max_length=250, null=False)
    contenido = models.CharField(max_length=2000, null=False)
    imagen = models.FileField(upload_to='imagenes/')
    publicador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publicador")

    def __str__(self):
        return f"{self.fecha_publicacion} - {self.titulo} ({self.publicador})"

"""class LeerMasTarde(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario")
    publicaciones = models.ManyToManyField(Articulo) 

    def __str__(self):
        return f"{self.usuario} - {self.publicaciones}" """  

class Categoria(models.Model):
    descripcion = models.CharField(max_length=64, null=False)

    def __str__(self):
        return f"{self.descripcion}"

class Producto(models.Model):
    titulo = models.CharField(max_length=128, null=False)
    imagen = models.FileField(upload_to='imagenes/')
    descripcion = models.CharField(max_length=1000, null=False)
    precio = models.FloatField(null=False)                       # models.DecimalField(..., max_digits=5, decimal_places=2) models.FloatField
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="clasificacion_categoria")

    #def __str__(self):
        #return f"{self.categoria} - {self.titulo}"
        #return f"{self.categoria} - {self.titulo} ({self.precio})"

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario")
    listado_productos = models.ManyToManyField(Producto)
    #publicaciones = models.ManyToManyField(Articulo)
    #vuelos = models.ManyToManyField(Vuelo, blank=True, related_name="pasajeros")
    total_carrito = models.FloatField(null=False)

    def __str__(self):
        return f"{self.usuario} {self.listado_productos}"