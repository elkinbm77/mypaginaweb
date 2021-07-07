from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
from .models import Articulo, Seccion
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models import Q

# Create your views here.

# Reserved.objects.filter(client=client_id).order_by('check_in')
# Reserved.objects.filter(client=client_id).order_by('-check_in')
# Reserved.objects.filter(client=client_id).order_by('check_in')[::-1]
# Reserved.objects.all().filter(client=client_id).order_by('check_in').reverse()

def index(request):
    if "leer_mas_tarde" not in request.session:
        request.session["leer_mas_tarde"] = []
        #User.objects.all().order_by( class="hljs-comment">'-id')[:10]
        #print(queryset)
    return render(request,"tienda/index.html", {
        "articulos_ppales": Articulo.objects.all().order_by('-fecha_publicacion')[0:3],
        "articulos_sdarios": Articulo.objects.all().order_by('-fecha_publicacion')[3:10],
        "lista_articulos": Articulo.objects.all().order_by('-fecha_publicacion'),
        "lista_secciones": Seccion.objects.all(),
        "leer_mas_tarde": request.session["leer_mas_tarde"],
    })

def about(request):
    return render(request,"tienda/about.html")

def contact(request):
    return render(request,"tienda/contact.html")

def newproduct(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = FormArticulo(request.POST, request.FILES, instance=Articulo(imagen=request.FILES['imagen'], publicador=user))      
        if form.is_valid():
            form.save()
            return redirect("sitio:index")          
    else:
        form = FormArticulo(initial={'fecha_publicacion':timezone.now()})
        return render(request, "tienda/newproduct.html", {
            "form": form
        })

def articulo(request, articulo_id):
    un_articulo = get_object_or_404(Articulo, id=articulo_id)
    return render(request, "tienda/articulo.html", {
        "articulo": un_articulo
    })

def articulo_alta(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = FormArticulo(request.POST, request.FILES, instance=Articulo(imagen=request.FILES['imagen'], publicador=user))      
        if form.is_valid():
            form.save()
            return redirect("sitio:index")          
    else:
        form = FormArticulo(initial={'fecha_publicacion':timezone.now()})
        return render(request, "tienda/articulo_nuevo.html", {
            "form": form
        })

def articulo_editar(request, articulo_id):
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
        })

def articulo_eliminar(request, articulo_id):
    un_articulo = get_object_or_404(Articulo, id=articulo_id)
    un_articulo.delete()
    return redirect("sitio:index")

def filtro_secciones(request, seccion_id):
    una_seccion = get_object_or_404(Seccion, id=seccion_id)
    queryset = Articulo.objects.all()
    queryset = queryset.filter(seccion=una_seccion)
    return render(request,"tienda/busqueda.html", {
        "lista_articulos": queryset,
        "lista_secciones": Seccion.objects.all(),
        "seccion_seleccionada": una_seccion
    })

def filtro_articulos(request):
    if request.method == "GET":     
        una_busqueda = request.GET.get("busqueda")
        print(una_busqueda)
        queryset = Articulo.objects.all() 
        if una_busqueda:
            queryset = Articulo.objects.filter(
                Q(titulo__icontains = una_busqueda) |
                Q(contenido__icontains = una_busqueda)
            ).distinct()
        return render(request,"tienda/busqueda.html", {
            "lista_articulos": queryset,
            "palabra_buscada": una_busqueda
        })   

@login_required
def leer_mas_tarde(request, articulo_id):
    un_articulo = get_object_or_404(Articulo, id=articulo_id)
    for id in request.session["leer_mas_tarde"]:
        if id == articulo_id:
            print(articulo_id)
            print("existe el articulo!!")
            #existe el articulo
            return HttpResponseRedirect(reverse("sitio:articulo", args=(un_articulo.id,))) 
        else:
            print("NO existe el articulo")
                     
    request.session["leer_mas_tarde"] += [articulo_id]
    return HttpResponseRedirect(reverse("sitio:articulo", args=(un_articulo.id,)))  

"""
def reserva(request, vuelo_id):
    if request.method == "POST":
        vueloId = Vuelo.objects.get(pk=vuelo_id)
        pasajeroId = int(request.POST["pasajero"])
        unPasajero = Pasajero.objects.get(pk=pasajeroId)
        unPasajero.vuelos.add(vueloId)
        return HttpResponseRedirect(reverse("vuelo", args=(vuelo_id,)))
"""

""" def articulo_alta(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = FormArticulo(request.POST, request.FILES, instance=Articulo(imagen=request.FILES['imagen'], publicador=user))      
        if form.is_valid():
            form.save()
            return redirect("sitio:index")          
    else:
        form = FormArticulo(initial={'fecha_publicacion':timezone.now()})
        return render(request, "tienda/articulo_nuevo.html", {
            "form": form
        }) """

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
