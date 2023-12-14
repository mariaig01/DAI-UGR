from pydantic import BaseModel, FilePath, Field, EmailStr, field_serializer, field_validator, ValidationError
from pydantic.functional_validators import AfterValidator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests, os, pathlib 


def consulta_1(productos_collection):
  #Consulta 1: Electrónica entre 100 y 200€, ordenados por precio

  consulta = productos_collection.find({
    "categoría": "electronics",
    "precio": { "$gt": 100, "$lt": 200 }
  })

  return consulta

def consulta_2(productos_collection):
  #Consulta 2: Productos que contengan la palabra 'pocket' en la descripción


  consulta = productos_collection.find({
    "descripción": { "$regex": "pocket|Pocket" }
  })

  return consulta

def consulta_3(productos_collection):
  #Consulta 3: Productos con puntuación mayor de 4


  consulta = productos_collection.find({
    "rating.puntuación": { "$gt": 4.0 }
  })

  return consulta

def consulta_4(productos_collection):
  #Consulta 4: Ropa de hombre, ordenada por puntuación


  consulta = productos_collection.find({
    "categoría": "men's clothing"
  }).sort("rating.puntuación", 1)

  return consulta



def facturacion_por_categoria(compras_collection, productos_collection):
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

  return facturacion_por_categoria


def calcular_facturacion(compras_collection, productos_collection):
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

