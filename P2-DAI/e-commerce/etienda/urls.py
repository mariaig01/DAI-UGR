from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from . import views
from .api import api

urlpatterns = [
    path("", views.index, name="index"),
    path("buscar", views.busqueda, name="busqueda"),
    path("busqueda_categoria/<str:categoria>/", views.categoria, name="busqueda_categoria"),
    path("nuevoproducto/", staff_member_required(views.nuevoprod), name="nuevoprod"),
    path("api/", api.urls),
]