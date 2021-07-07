from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
from .models import Producto, Categoria, Carrito
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models import Q

# Create your views here.

# Reserved.objects.filter(client=client_id).order_by('check_in')
# Reserved.objects.filter(client=client_id).order_by('-check_in')
# Reserved.objects.filter(client=client_id).order_by('check_in')[::-1]
# Reserved.objects.all().filter(client=client_id).order_by('check_in').reverse()

# User.objects.all().order_by( class="hljs-comment">'-id')[:10]
# print(queryset)

def index(request):
    if "carrito" not in request.session:
        request.session["carrito"] = []
    return render(request,"tienda/index.html", {
        "productos_ppales": Producto.objects.all().order_by('-id')[0:3],
        "productos_sdarios": Producto.objects.all().order_by('-id')[3:10],
        "lista_productos": Producto.objects.all().order_by('-id'),
        "lista_categorias": Categoria.objects.all(),
        "carrito": request.session["carrito"],
    })

def producto(request, producto_id):
    un_producto = get_object_or_404(Producto, id=producto_id)
    return render(request, "tienda/articulo.html", {
        "producto": un_producto
    })

def about(request):
    return render(request,"tienda/about.html")

def contact(request):
    return render(request,"tienda/contact.html")


"""def producto(request, producto_id):
    un_producto = get_object_or_404(Producto, id=producto_id)
    queryset = Producto.objects.all()
    print(queryset)
    queryset = queryset.filter(id=producto_id)
    print(queryset)
    if un_producto:
        print("un_producto:")
        print(un_producto)
        un_producto = producto_id
        print(producto_id) 
        print("un_producto:")
        print(un_producto) 
    return render(request, "tienda/articulo.html", {
        "producto": queryset
    })"""

def producto_alta(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = FormProducto(request.POST, request.FILES, instance=Producto(imagen=request.FILES['imagen']))      
        if form.is_valid():
            form.save()
            return redirect("sitio:index")  # ERROR 
            #return redirect("index.html")         
    else:
        form = FormProducto()
        return render(request, "tienda/producto_nuevo.html", {
            "form": form
        })

"""
def producto_editar(request, producto_id):
    un_producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":  
        user = User.objects.get(username=request.user)   
        un_producto.publicador = user
        form = FormProducto(data=request.POST, files=request.FILES, instance=un_producto)
        if form.is_valid():
            form.save()
            return redirect("sitio:index")
    else:
        form = FormProducto(instance = un_producto)
        return render(request, 'tienda/producto_edicion.html', {
            "producto": un_producto,
            "form": form
        })
"""

def producto_editar(request, producto_id):
    un_producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":  
        #user = User.objects.get(username=request.user)   
        #un_producto.publicador = user
        form = FormProducto(data=request.POST, files=request.FILES, instance=un_producto)
        if form.is_valid():
            form.save()
            return redirect("sitio:index")  
    else:
        form = FormProducto(instance = un_producto)
        return render(request, 'tienda/producto_edicion.html', {
            "producto": un_producto,
            "form": form
        })

def producto_eliminar(request, producto_id):
    un_producto = get_object_or_404(Producto, id=producto_id)
    un_producto.delete()
    return redirect("sitio:index")

def filtro_categorias(request, categoria_id):
    una_categoria = get_object_or_404(Categoria, id=categoria_id)
    queryset = Producto.objects.all()
    queryset = queryset.filter(categoria=una_categoria)
    return render(request,"tienda/busqueda.html", {
        "lista_productos": queryset,
        "lista_categorias": Categoria.objects.all(),
        "categoria_seleccionada": una_categoria
    })

def filtro_productos(request):
    if request.method == "GET":     
        una_busqueda = request.GET.get("busqueda")
        print(una_busqueda)
        queryset = None 
        if una_busqueda:
            queryset = Producto.objects.filter(
                Q(titulo__icontains = una_busqueda) |
                Q(descripcion__icontains = una_busqueda)
            ).distinct()
        return render(request,"tienda/busqueda.html", {
            "lista_productos": queryset,
            "palabra_buscada": una_busqueda
        })   

@login_required
def carrito(request, producto_id):  # Agregar producto al carrito de compras
    un_producto = get_object_or_404(Producto, id=producto_id)
    for id in request.session["carrito"]:
        if id == producto_id:
            print(producto_id)
            print("existe el producto!!")
            #existe el producto
            return HttpResponseRedirect(reverse("sitio:producto", args=(un_producto.id,))) 
        else:
            print("NO existe el producto")
                     
    request.session["carrito"] += [producto_id]
    return HttpResponseRedirect(reverse("sitio:producto", args=(un_producto.id,)))




#@login_required
def consultar_carrito(request): 
    miLista = []
    #un_producto = get_object_or_404(producto, id=producto_id)
    for id in request.session["carrito"]:
        id_product = id
        queryset = Producto.objects.all()
        queryset = queryset.filter(id=id_product)
        print(id)
        print(id_product)
        if queryset:
            print(queryset)
            miLista.append = ((queryset.id, queryset.titulo, queryset.precio))
            print(miLista)
            return render(request,"tienda/busqueda.html", {
                        #"lista_productos": queryset,
                        #"palabra_buscada": una_busqueda,
                        miLista
                    })



def consulta_carrito(request): #consultar productos agregados al carrito de compras
    if "carrito" not in request.session:
        request.session["carrito"] = []
    return render(request,"tienda/consulta_carrito.html", {
        "carrito": request.session["carrito"],
    })



"""
def reserva(request, vuelo_id):
    if request.method == "POST":
        vueloId = Vuelo.objects.get(pk=vuelo_id)
        pasajeroId = int(request.POST["pasajero"])
        unPasajero = Pasajero.objects.get(pk=pasajeroId)
        unPasajero.vuelos.add(vueloId)
        return HttpResponseRedirect(reverse("vuelo", args=(vuelo_id,)))
"""

"""def articulo_editar(request, articulo_id):
    un_articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.method == "POST":  
        user = User.objects.get(username=request.user)   
        un_articulo.publicador = user
        form = FormArticulo(data=request.POST, files=request.FILES, instance=un_articulo)
        if form.is_valid():
            form.save()
            return redirect("sitio:index")
    else:
        form = FormArticulo(instance = un_articulo)
        return render(request, 'tienda/articulo_edicion.html', {
            "articulo": un_articulo,
            "form": form
        })"""
