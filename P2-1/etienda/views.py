from django.shortcuts import render
from django.http import HttpResponse
from .models import Nota, Producto, Compra
from .queries import consulta_1, consulta_2, consulta_3, consulta_4, calcular_facturacion, facturacion_por_categoria
# Create your views here

def index(request):
    html = """
    <body>
        <h1 style="font-size: 20px;">DAI: Práctica 2</h1>
        <ol> 
            <li> <a href="Consulta1/">Consulta 1: Electrónica entre 100 y 200€, ordenados por precio</a> </li>
            <li> <a href="Consulta2/">Consulta 2: Productos que contengan la palabra 'pocket' en la descripción</a> </li>
            <li> <a href="Consulta3/">Consulta 3: Productos con puntuación mayor de 4</a> </li>
            <li> <a href="Consulta4/">Consulta 4:Ropa de hombre, ordenada por puntuación </a> </li>
            <li> <a href="Consulta5/">Consulta 5: Facturación total</a> </li>
            <li> <a href="Consulta6/">Consulta 6: Facturación por categoría de producto</a> </li>
        </ol>
    </body>

    """
    return HttpResponse(html)

def Consulta1(request):
    salida = consulta_1()
    return HttpResponse(salida, content_type="text/plain")

def Consulta2 (request):
    salida = consulta_2()
    return HttpResponse(salida, content_type="text/plain")

def Consulta3 (request):
    salida = consulta_3()
    return HttpResponse(salida, content_type="text/plain")

def Consulta4 (request):
    salida = consulta_4()
    return HttpResponse(salida, content_type="text/plain")

def Consulta5 (request):
    salida = calcular_facturacion()
    return HttpResponse(salida, content_type="text/plain")

def Consulta6 (request):
    salida = facturacion_por_categoria()
    return HttpResponse(salida, content_type="text/plain") 









