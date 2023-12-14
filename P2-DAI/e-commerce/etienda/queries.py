from .models import Nota, Producto, Compra, getProductos
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests, os, pathlib # request: solicitudes HTTP a API externa, os: trabajar con el sistema operativo, pathlib: trabajar con rutas de archivos
import re
import json
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
		

# Conexión con la BD (conexión con MongoDB)	
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Creamos una base de datos llamada tienda
productos_collection = tienda_db.productos  # establecen una conexión con la base de datos MongoDB y crean una colección llamada productos
productos_collection.delete_one({"nombre": 'string'})

#Función que devuelve los productos de la BD
def Productos()	:
	return productos_collection.find()


def busqueda(termino_busqueda):
    # Realizar una búsqueda en la colección de productos
    resultados = productos_collection.find({
        "$or": [
            {"nombre": {"$regex": termino_busqueda, "$options": "i"}},
            {"descripción": {"$regex": termino_busqueda, "$options": "i"}}
        ]
    })

    # Devolver los resultados de la búsqueda
    return resultados

def busqueda_categoria(categoria):
    resultado = productos_collection.find({"categoría": categoria})
    return resultado


def CategoriasProductos():
	return list(productos_collection.distinct("categoría"))


def ultimoID(productos_collection):
    lastID = productos_collection.find_one(sort=[("productoid", -1)])
    return lastID["productoid"]


#Funciones para la API
def lista_productos():
    products = productos_collection.find()
    result = []
    for p in products:
        p["id"] = str(p.get("_id"))
        del p["_id"]
        p["title"] = p.get("nombre")
        p["price"] = p.get("precio")
        p["description"] = p.get("descripción")  
        p["category"] = p.get("categoría") 
        p["rating"] = {"rate": p["rating"]["puntuación"], "count": p["rating"]["cuenta"]} 
        
        result.append(p)
    return result


#Funcion que busca un producto por el id normal, es decir, en mi caso el productoid
def producto_id_normal(id):
    product = productos_collection.find_one({'productoid': id})
    product["id"] = str(product.get("_id"))
    product["title"] = product.get("nombre")
    product["price"] = product.get("precio")
    product["description"] = product.get("descripción")  
    product["category"] = product.get("categoría") 
    product["rating"] = {"rate": product["rating"]["puntuación"], "count": product["rating"]["cuenta"]}
    return product

#Funcion que busca un producto por el id de mongodb
def producto_id(id):
    product = productos_collection.find_one({'_id': ObjectId(id)})
    product["id"] = str(product.get("_id"))
    del product["_id"]
    product["title"] = product.get("nombre")
    product["price"] = product.get("precio")
    product["description"] = product.get("descripción")  
    product["category"] = product.get("categoría") 
    product["rating"] = {"rate": product["rating"]["puntuación"], "count": product["rating"]["cuenta"]}
    return product


#si a count no le pongo un numero no se inserta
def insertar_producto(producto):
    #Como mi clase de models.py está definida en español, tengo que cambiar los nombres de los campos para que coincidan con los de la BD
    try:
        p = {
            "productoid":  ultimoID(productos_collection)+1,
            'nombre': producto.title,
            'precio': producto.price,
            'descripción': producto.description,
            'categoría': producto.category,
            'imágen': "image",
            'rating': {'puntuación': producto.rating.rate, 'cuenta': producto.rating.count}
        }
        
        product = Producto(**p)


        productos_collection.insert_one(product.dict())
        return producto_id_normal(product.productoid)
    
    except Exception as e:
        logger.error(e)
        logger.info("El producto no ha podido ser insertado")
    


def modificar_producto(id, producto):
    try:
        productos_collection.update_one({"_id": ObjectId(id)}, {"$set": {"nombre": producto.title, "precio": producto.price, "descripción": producto.description, "categoría": producto.category, "imágen": "image", "rating": {"puntuación": producto.rating.rate, "cuenta": producto.rating.count}}})
        logger.info("El producto ha sido modificado correctamente")
        return producto_id(id)
    except Exception as e:
        logger.error(e)
        logger.info("El producto no ha podido ser modificado")
    

def elimina_prod(id):
    try:
        productos_collection.delete_one({'_id': ObjectId(id)})
        
    except Exception as e:
        logger.info("El producto no ha podido ser eliminado")


def puntuar(id, rating):
    try:
        #obtiene el producto
        producto = productos_collection.find_one({'productoid': id})
        
        #obtenemos su rating
        puntuacion = producto["rating"]
        cuenta = puntuacion["cuenta"] + 1
        nueva_puntuacion = puntuacion["puntuación"] * puntuacion["cuenta"] + rating
        media = nueva_puntuacion/ cuenta
        
        productos_collection.update_one({"productoid": id},{"$set": {"rating": {"puntuación": media, "cuenta":cuenta}}})
        return producto_id_normal(id)
    
    except Exception as e:
        logger.info("La puntuación no ha podido ser modificada")

