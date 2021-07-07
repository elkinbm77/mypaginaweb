from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
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
    print("request session carrito")
    print(request.session["carrito"]) 
    print(len(request.session["carrito"]))   
    return render(request,"tienda/index.html", {
        "productos_ppales": Producto.objects.all().order_by('-id')[0:3],
        "productos_sdarios": Producto.objects.all().order_by('-id')[3:10],
        #"lista_productos": Producto.objects.all().order_by('-id'),
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

@login_required
def producto_alta(request):
    if request.method == "POST":
        #user = User.objects.get(username=request.user)
        form = FormProducto(request.POST, request.FILES, instance=Producto(imagen=request.FILES['imagen']))      
        if form.is_valid():
            form.save()
            return redirect("sitio:index")  # ERROR 
            #return HttpResponseRedirect(reverse("sitio:index")         
    else:
        form = FormProducto()
        return render(request, "tienda/producto_nuevo.html", {
            "form": form
        })

@login_required
def producto_editar(request, producto_id):
    un_producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":  
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

@login_required
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
        #print(una_busqueda)
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
            #print(producto_id)
            print("existe el producto!!")
            #existe el producto
            request.session["carrito"]             
            return HttpResponseRedirect(reverse("sitio:producto", args=(un_producto.id,))) 
        else:
            print("NO existe el producto")
                     
    request.session["carrito"] += [producto_id]

    return HttpResponseRedirect(reverse("sitio:producto", args=(un_producto.id,))) 

#lista.remove(elemento)
#lista.pop(posición)
#del lista[posicion]

@login_required
def carrito_quitar(request):
    producto_id = 10
    print ("producto_id en carrito_quitar")
    print (producto_id)
    return render(request,"tienda/actualiza_carrito.html", {
        "actual_carro": producto_id
    })

@login_required
def carrito_eliminar(request):  # Vaciar el carrito de compras
    producto_id = 10
    #un_producto = get_object_or_404(Producto, id=producto_id)
    print(len(request.session["carrito"]))
    print(len(request.session["carrito"]))
    while len(request.session["carrito"])>0:
        request.session["carrito"].pop()
        print("request session carrito se está vaciando")
    request.session.modified = True
    print(request.session["carrito"])
    #existe el producto
    return render(request,"tienda/elimina_carrito.html", {
        "elimi_carro": producto_id
    })
"""
def carrito_quitar(request, producto_id):  # Quitar producto al carrito de compras
    un_producto = get_object_or_404(Producto, id=producto_id)
    for id in request.session["carrito"]:
        if id == producto_id:
            print(producto_id)
            print("existe el producto!!")
            #existe el producto
            return HttpResponseRedirect(reverse("sitio:producto", args=(un_producto.id,)))
            #request.session["carrito"] += [producto_id] 
            #"request.session["carrito"].pop()"
            request.session["carrito"].remove(producto_id)
        else:
            print("NO existe el producto")
    return redirect("sitio:index")
    #return render(request,"tienda/consulta_carrito.html")                 
    #request.session["carrito"] += [producto_id]
    #return HttpResponseRedirect(reverse("sitio:producto", args=(un_producto.id,))) 
"""

@login_required
def consultar_carrito(request): #consultar productos agregados al carrito de compras por su ID y trae de la BD los demas campos a mostar
    miLista = []
    queryset = Producto.objects.all()
    for id in request.session["carrito"]:
        producto_id = id
        #-----------------------------------------------------
        un_producto = get_object_or_404(Producto, id=producto_id)
        queryset = Producto.objects.filter(id = producto_id)
        if queryset:
            for q in queryset:
                 print (q.titulo)
                 miLista.append((id, q.titulo, q.precio))
            #print(miLista)
        else:
            print("NO wxiste")
    return render(request,"tienda/consulta_carrito.html", {
        "carrito2": miLista,
        "consulta_carro": queryset
    })
        #-----------------------------------------------------

@login_required
def consulta_carrito(request): #consultar productos agregados al carrito de compras (solo los ID)
    if "carrito" not in request.session:
        request.session["carrito"] = []
    return render(request,"tienda/consulta_carrito.html", {
        "carrito": request.session["carrito"],
    })

def envia_correo(request):  # Vaciar el carrito de compras
    return render(request,"tienda/enviar_correo.html")

"""
print(Seller.objects.all().query)
SELECT "app_seller"."id", "app_seller"."name" FROM "app_seller"
"""   
"""
def reserva(request, vuelo_id):
    if request.method == "POST":
        vueloId = Vuelo.objects.get(pk=vuelo_id)
        pasajeroId = int(request.POST["pasajero"])
        unPasajero = Pasajero.objects.get(pk=pasajeroId)
        unPasajero.vuelos.add(vueloId)
        return HttpResponseRedirect(reverse("vuelo", args=(vuelo_id,)))
"""
