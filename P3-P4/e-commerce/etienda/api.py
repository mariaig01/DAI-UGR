
from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema
from .queries import insertar_producto, lista_productos, producto_id, modificar_producto, elimina_prod, puntuar, producto_id_normal 
from typing import Optional
from ninja.security import django_auth
from ninja.security import HttpBearer
from typing import List

import logging
logger = logging.getLogger(__name__)



# class GlobalAuth(HttpBearer):
#     def authenticate(self, request, token):
#         if token == "supersecret":
#             return token
		
# api = NinjaExtraAPI(auth=GlobalAuth())


api = NinjaExtraAPI()
	
class Rate(Schema):
	rate: float
	count: int
	
class ProductSchema(Schema):  # sirve para validar y para documentación
	id:    str
	title: str
	price: float
	description: str
	category: str
	image: str = None
	rating: Rate
	
	
class ProductSchemaIn(Schema):
	title: str
	price: float
	description: str
	category: str
	rating: Rate
	
	
class ErrorSchema(Schema):
	message: str
	
class SuccessResponseSchema(Schema):
    message: str


# Lista Productos
@api.get("/listaproductos", tags=['Lista productos'],response={202: list[ProductSchema], 404:ErrorSchema})
def lista_prod(request, desde: Optional[int] = 0, hasta: Optional[int] = 10):
	try:
		qs = lista_productos()
		resultados = qs[desde:hasta]
		return 202,resultados
	except:
		return 404, {'message': 'no encontrado'}

#Añadir Producto
@api.post("/añadirproducto", tags=['Add product'],response={202: ProductSchema, 404:ErrorSchema})
def insertar_prod(request, payload: ProductSchemaIn):
    try:
        prod = insertar_producto(payload)
        return 202, prod
    
    except:
        return 404, {'message': 'No ha podido ser insertado'}

# Detalle Producto
@api.get("etienda/detalleproducto/{id}", tags=['Detalle Producto'],response={202: ProductSchema, 404:ErrorSchema})
def lista_prod(request,id: str):
	try:
		qs = producto_id(id)
		return 202,qs
	except:
		return 404, {'message': 'no encontrado'}


#Modifica producto
@api.put("/productos/{id}", tags=['Modifica Producto'], response = {202: ProductSchema, 404: ErrorSchema})
def Modifica_producto(request, id: str, payload: ProductSchemaIn):
	try:
		for attr, value in payload.dict().items():
			logger.debug(f'{attr} -> {value}')
			# modificar DB
			prod = modificar_producto(id, payload)
		return 202,prod
	except:
		return 404, {'message': 'no encontrado'}



#borra un producto de la BD
@api.delete('/elimina', tags=['Elimina producto'])
def EliminarProducto(request, id : str):
	try:
		resultado = elimina_prod(id)
		return 200, resultado
	except Exception as e:
		logger.error(e)
		return 404, {"message": "No se ha encontrado el producto"}


#modifica la puntuacion de un producto
@api.put("/puntuar/{id}/{rating}", tags=['Modifica puntuacion'], response={202: ProductSchema, 404: ErrorSchema})
def modify_rating(request, id: int, rating: int):
    try:
        resultado = puntuar(id, rating)
        return 202, resultado
    
    except:
        return 404, {"message": "the product rate could not be modified"}


#obtiene el producto por el id por defecto
@api.get('/idproducto/{id}', tags=['Get id'], response={202: ProductSchema, 404: ErrorSchema})
def get_product(request, id:int):
    try:
        product = producto_id_normal(id)
        return 202, product
    except:
        return 404, {'message': 'the product could not be found'}