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



















# from pydantic import BaseModel, FilePath, Field, EmailStr
# from pymongo import MongoClient
# from pprint import pprint
# from datetime import datetime
# from typing import Any
# import requests
# import os


# def imprime_query(query):
# 	for x in query:
# 		print(x)
	

# def get_quantities():
# 	ids_quantities = []
# 	compras_totales = compras_collection.find()

# 	for c in compras_totales:
# 		pc = c.get('products')
# 		for p in pc:
# 			ids_quantities.append([p.get('productId'), p.get('quantity')])
	
# 	return ids_quantities

# def get_price_and_quantity(id):
# 	prod = productos_collection.find_one({"_id":lista_productos_ids[id]})
# 	price_prod = prod.get('price')
# 	category = prod.get('category')

# 	return price_prod, category

# def calcula_facturacion():
# 	facturacion_total = 0

# 	ids_quantities = get_quantities()
	
# 	for id in ids_quantities:
# 		id_on_list = id[0]-1 # los id de los productos empiezan en 1
		
# 		price_prod, category = get_price_and_quantity(id_on_list)

# 		facturacion_total += price_prod*id[1] # Cantidad comprada por precio
# 	return facturacion_total
		
# def facturacion_por_categoria():
# 	facturacion_total_categoria = {}
# 	categories = productos_collection.distinct("category")
# 	for c in categories:
# 		facturacion_total_categoria[c] = 0

# 	ids_quantities = get_quantities()

# 	for id in ids_quantities:
# 		id_on_list = id[0]-1 # los id de los productos empiezan en 1
# 		price_prod, category = get_price_and_quantity(id_on_list)
# 		facturacion_total_categoria[category] += price_prod*id[1] # Cantidad comprada por precio de cada categoria

# 	return facturacion_total_categoria


# # Conexión con la BD				
# # https://pymongo.readthedocs.io/en/stable/tutorial.html
# client = MongoClient('mongo', 27017)

# tienda_db = client.tienda                   # Base de Datos
# productos_collection = tienda_db.productos  # Colección  
# compras_collection = tienda_db.compras  # Colección


# ## todos los productos
# lista_productos_ids = []
# for prod in productos_collection.find():
# 	lista_productos_ids.append(prod.get('_id')) # autoinsertado por mongo
	
# separacion = "---------------------------------"
# ###### CONSULTA
# print(separacion,"\n\tElectrónica entre 100 y 200€, ordenados por precio\n")
# query = {"category": "electronics", "price": {"$gt":100, "$lt":200}}
# imprime_query(productos_collection.find(query,{"_id":0, "title": 1, "price": 1}).sort("price", 1))

# #    Productos que contengan la palabra 'pocket' en la descripción
# print(separacion,"\n\tProductos que contengan la palabra 'pocket' en la descripción\n" )
# #options i -> match upper and lower cases
# query2 = {"description": {"$regex" : "pocket", "$options": "i"}}
# imprime_query(productos_collection.find(query2,{"_id":0, "title": 1}))

# #    Productos con puntuación mayor de 4
# print(separacion,"\n\tProductos con puntuación mayor de 4\n")
# query3= {"rating.rate": {"$gt":4}}
# imprime_query(productos_collection.find(query3,{"_id":0, "title": 1, "rating":1}))

# #    Ropa de hombre, ordenada por puntuación
# print(separacion,"\n\tRopa de hombre, ordenada por puntuación\n")
# query4={"category": "men's clothing"}
# imprime_query(productos_collection.find(query4,{"_id":0, "title": 1, "category":1, "rating":1}).sort("rating.rate", 1))

# #    Facturación total
# print(separacion, "\n\tFacturación total\n")
# facturacion_total = calcula_facturacion()
# print("Facturación total: ", round(facturacion_total,2), "€")

# #    Facturación por categoría de producto
# print(separacion,"\n\tFacturación por categoria de producto\n")
# print("Facturación por categoria: ")

# pprint(facturacion_por_categoria())


# ## PARA NOTA ##
# #docker compose run --rm -v "$(pwd)/backup:/backup" mongo bash -c 'mongodump 
# #--host mongo --port 27017 --db tienda --gzip --archive=/backup/backup.gz'
# #2023-10-05T16:30:11.803+0000    writing tienda.compras to archive '/backup/backup.gz'
# #2023-10-05T16:30:11.807+0000    writing tienda.productos to archive '/backup/backup.gz'
# #2023-10-05T16:30:11.807+0000    done dumping tienda.compras (7 documents)
# #2023-10-05T16:30:11.809+0000    done dumping tienda.productos (20 documents)




