from django.db import models
from pymongo import MongoClient
from pydantic import BaseModel, FilePath, Field, EmailStr, field_serializer, field_validator, ValidationError
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests, os, pathlib

def getProductos(api):
	response = requests.get(api)
	return response.json()
				

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

