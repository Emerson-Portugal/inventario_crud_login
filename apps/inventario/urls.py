# inventario/urls.py
from django.urls import path
from . import views

app_name = 'inventario'  

urlpatterns = [

    path('', views.product_crud, name='product_crud'),
    
    path('registrarProducto/', views.registrarProducto, name='registrarProducto'),

    path('edicionProducto/<str:codigo>/', views.edicionProducto, name='edicionProducto'),

    path('editarProducto/', views.editarProducto, name='editarProducto'),

    path('eliminarProducto/<str:codigo>/', views.eliminarProducto, name='eliminarProducto'),

    path('cargar-inventario/', views.cargar_inventario, name='cargar_inventario'),

    path('buscar-producto/', views.listar_producto, name='buscarProducto'),




]
