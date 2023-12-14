from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Nota, Producto, Compra
from . import queries
from . import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ProductoForm
import pathlib
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)

# Create your views here

def index(request):
    context = {'productos' : queries.productos_collection.find(),'categorias' : queries.CategoriasProductos()}
    return render(request, 'etienda/index.html', context) 

def busqueda(request):
    context = {'consulta' : request.GET.get('busqueda', ''), 'productos' : queries.busqueda(request.GET.get('busqueda', '')), 'categorias' : queries.CategoriasProductos()}
    return render(request, 'etienda/busqueda.html', context) 


def categoria(request, categoria):
    context = {'productos' : queries.busqueda_categoria(categoria), 'categorias' : queries.CategoriasProductos(), 'categoria' : categoria}
    return render(request, 'etienda/categoria.html', context)



@staff_member_required
def nuevoprod(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            name_file = handle_file(request.FILES['image'])
            # construyo el producto
            p = {
                "productoid": queries.productos_collection.find_one(sort=[("productoid", -1)])["productoid"]+1,
                "nombre": form.cleaned_data["title"],
                "precio": form.cleaned_data["price"],
                "descripción": form.cleaned_data["description"],
                "categoría": form.cleaned_data["category"],
                "imágen":"imágenes/" + name_file,
                "rating": {'puntuación':1.0, 'cuenta': 1.0}
            }
            prod = Producto(**p)
            logger.info('Adding product to the database')
            # Inserta el producto en la BD
            queries.productos_collection.insert_one(prod.dict())
            messages.success(request, 'The addition of the product was successful.')

            # Crear un nuevo formulario vacío
            form = ProductoForm()
        else:
            messages.error(request, 'The addition of the product was unsuccessful.')
            messages.warning(request, 'The title should commence with an initial capital letter.')
            messages.warning(request, 'The price cannot be negative.')
    else:
        form = ProductoForm()

    context = {'form': form, 'categorias': queries.CategoriasProductos()}
    return render(request, 'etienda/nuevoprod.html', context)



def handle_file(file):
    path = 'imágenes/' + file.name
    with open(path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file.name
