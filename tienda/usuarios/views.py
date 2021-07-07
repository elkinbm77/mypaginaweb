from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import *

# Create your views here.

def registrarse(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            print(HttpResponseRedirect(reverse('login')))          
            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {
        'form': form
        })

"""
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
"""