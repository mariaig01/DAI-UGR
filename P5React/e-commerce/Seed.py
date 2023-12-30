# Seed.py
from pydantic import BaseModel, FilePath, Field, EmailStr, field_serializer, field_validator, ValidationError
from pydantic.functional_validators import AfterValidator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests, os, pathlib # request: solicitudes HTTP a API externa, os: trabajar con el sistema operativo, pathlib: trabajar con rutas de archivos
import queries
import re
		
# https://requests.readthedocs.io/en/latest/

def getProductos(api):
	response = requests.get(api)
	return response.json()
				
# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/

#Copia de seguridad: mongodump --host localhost --port 27017 --db tienda

class Nota(BaseModel):
	puntuación: float = Field(ge=0., lt=5.)
	cuenta: int = Field(ge=1)


class Producto(BaseModel):
	_id: Any
	productoid: int
	nombre: str
	precio: float
	descripción: str
	categoría: str
	imágen: FilePath | None
	rating: Nota

	@field_serializer('imágen')
	def serializaPath(self, val) -> str:
		if type(val) is pathlib.PosixPath:
			return str(val)
		return val	
	@field_validator('nombre')
	@classmethod
	def mayuscula_validator(cls,titulo) -> str:
		if not titulo[0].isupper():
				raise ValueError('La primera letra del nombre debe empezar por mayúscula')
		return titulo.title()


class Compra(BaseModel):
	_id: Any
	usuario: EmailStr
	fecha: datetime
	productos: list		


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
	directorio = "imágenes/"
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
		'imágen': FilePath("imágenes/" + nombre_imagen),
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



print("\n\n\n\n")

#Consultas

print("Electrónica entre 100 y 200€, ordenados por precio \n")

consulta = queries.consulta_1(productos_collection)

for producto in consulta:
	print(f"{str(producto)}+\n")

print("\n\n\n")

print("Productos que contengan la palabra 'pocket' en la descripción \n")

consulta = queries.consulta_2(productos_collection)

for producto in consulta:
	print(f"{str(producto)}+\n")

print("\n\n\n")

print("Productos con puntuación mayor de 4\n")

consulta = queries.consulta_3(productos_collection)

for producto in consulta:
	print(f"{str(producto)}+\n")

print("\n\n\n")

print("Ropa de hombre, ordenada por puntuación\n")

consulta = queries.consulta_4(productos_collection)

for producto in consulta:
	print(f"{str(producto)}+\n")

print("\n")

facturacion = queries.calcular_facturacion(compras_collection,productos_collection)

print(f"Facturación: {facturacion:.2f}€ \n")


print("Facturación por categoría de producto:  ")

facturacion_por_categoria = queries.facturacion_por_categoria(compras_collection, productos_collection)

for categoria, facturacion in facturacion_por_categoria.items():
  print(f"\n{categoria}: {facturacion:.2f}€\n")









