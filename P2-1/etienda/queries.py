from .models import Nota, Producto, Compra, getProductos
from pydantic import BaseModel, FilePath, Field, EmailStr, field_serializer, field_validator, ValidationError
from pydantic.functional_validators import AfterValidator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests, os, pathlib # request: solicitudes HTTP a API externa, os: trabajar con el sistema operativo, pathlib: trabajar con rutas de archivos
import queries
import re
import json
		

# Conexión con la BD (conexión con MongoDB)	
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Creamos una base de datos llamada tienda
productos_collection = tienda_db.productos  # establecen una conexión con la base de datos MongoDB y crean una colección llamada productos
				
#Obtenemos los datos de productos, compras y usuarios (para los emails del campo usuario de compras)
productos = getProductos('https://fakestoreapi.com/products') #obtenemos los datos de la api externa

productos_collection.drop()

compras_collection = tienda_db.compras  # Colección de las compras realizadas

#Obtiene las compras de la API
compras = getProductos('https://fakestoreapi.com/carts')

usuarios = getProductos('https://fakestoreapi.com/users')

compras_collection.drop()


#Inserción de productos y compras en MongoDB
for prod in productos:
	direccion = prod.get("image") 
	directorio = "imagenes/"
	nombre_imagen=pathlib.Path(direccion).name
	ruta = directorio+nombre_imagen
	response = requests.get(direccion)
	with open(ruta,"wb") as archivo:
		archivo.write(response.content)

	product = {
		'productoid': prod["id"],
		'nombre': prod["title"],
		'precio': prod["price"],
		'descripción': prod["description"],
		'categoría': prod["category"],
		'imágen': FilePath("imagenes/" + nombre_imagen),
		'rating': {'puntuación': prod["rating"]["rate"], 'cuenta': prod["rating"]["count"]}
	}

	prod = Producto(**product)

	try:
		productos_collection.insert_one(prod.model_dump())
	except Exception as e:
		print(e)



cont = 0
for comp in compras:
	c = {
		'usuario': usuarios[cont]["email"],
		'fecha': datetime.now(),
		'productos': comp["products"],
	}

	compra = Compra(**c)
	compras_collection.insert_one(compra.model_dump())
	cont+=1




def consulta_1():
  #Consulta 1: Electrónica entre 100 y 200€, ordenados por precio

  consulta = productos_collection.find({
    "categoría": "electronics",
    "precio": { "$gt": 100, "$lt": 200 }
  })

  return consulta

def consulta_2():
  #Consulta 2: Productos que contengan la palabra 'pocket' en la descripción


  consulta = productos_collection.find({
    "descripción": { "$regex": "pocket|Pocket" }
  })

  return consulta

def consulta_3():
  #Consulta 3: Productos con puntuación mayor de 4


  consulta = productos_collection.find({
    "rating.puntuación": { "$gt": 4.0 }
  })

  return consulta

def consulta_4():
  #Consulta 4: Ropa de hombre, ordenada por puntuación


  consulta = productos_collection.find({
    "categoría": "men's clothing"
  }).sort("rating.puntuación", 1)

  return consulta



def facturacion_por_categoria():
  #Calcula la facturación por categoría de producto.

  facturacion_por_categoria = {}

  for compra in compras_collection.find():
    for product in compra["productos"]:

      cantidad = product["quantity"]
      prod = productos_collection.find_one({"productoid": product["productId"] })
      precio = prod["precio"]

      categoria = prod["categoría"]

      if categoria not in facturacion_por_categoria:
        facturacion_por_categoria[categoria] = 0

      facturacion_por_categoria[categoria] += precio * cantidad

  return json.dumps(facturacion_por_categoria)


def calcular_facturacion():
  #Calcula la facturación total de todas las compras.

  facturacion = 0
  for compra in compras_collection.find():
    for producto in compra["productos"]:
      producto_id = producto["productId"]
      cantidad = producto["quantity"]

      p = productos_collection.find_one({"productoid": producto["productId"] })
      precio = p["precio"]

      facturacion += precio * cantidad

  return round(facturacion, 2)

