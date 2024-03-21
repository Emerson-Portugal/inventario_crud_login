from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .forms import UploadFileForm
from .models import InventarioExcel
import pandas as pd
import numpy as np 
from django.http import JsonResponse

from django import forms
from .models import Producto
from django.http import JsonResponse




from django.contrib import messages


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'cantidad', 'usuario']


# Insertar Valores y Filrado


def listar_producto(request):
    nombre = request.GET.get('nombre')

    if nombre:
        productos_listados = InventarioExcel.objects.filter(nombre__icontains=nombre)
    else:
        productos_listados = InventarioExcel.objects.all()

    productos_json = list(productos_listados.values('codigo', 'nombre', 'marca', 'tipo_existencia', 'stock_actual'))
    return JsonResponse(productos_json, safe=False)


def registrarProducto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        usuario = request.user

        if not codigo or not nombre or not cantidad:
            return JsonResponse({'success': False, 'message': 'Por favor completa todos los campos.'})
        elif Producto.objects.filter(codigo=codigo).exists():
            return JsonResponse({'success': False, 'message': '¡El código ya está en uso!'})
        else:
            Producto.objects.create(
                codigo=codigo, nombre=nombre, cantidad=cantidad, usuario=usuario)
            return JsonResponse({'success': True, 'message': '¡Producto Registrado!'})
    else:
        form = ProductoForm()
        return render(request, "product_crud.html", {'form': form})




















## LOGIN DEL SISTEMA INVENTARIO

@login_required
def product_crud(request):
    productos_listados = Producto.objects.all()
    mensajes = messages.get_messages(request)
    return render(request, 'product_crud.html', {"Productos": productos_listados, "messages": mensajes})

def home(request):
    productos_listados = Producto.objects.all()
    messages.success(request, '¡PRODUCTO LISTADO!')
    return render(request, "product_crud.html", {"Productos": productos_listados})








# CRUD del SISTEMA INVENTARIO

def edicionProducto(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    return render(request, "product_edit.html", {"Producto": producto})

def editarProducto(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        cantidad = request.POST['cantidad']
        usuario = request.user  # Capturar el usuario autenticado

        producto = Producto.objects.get(codigo=codigo)
        producto.nombre = nombre
        producto.cantidad = cantidad
        producto.usuario = usuario  # Asignar el usuario autenticado al producto
        producto.save()

        messages.success(request, '¡Producto actualizado!')

        return redirect(reverse('inventario:product_crud'))

    return redirect(reverse('inventario:product_crud'))

def eliminarProducto(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    producto.delete()

    messages.success(request, '¡Producto eliminado!')

    return redirect(reverse('inventario:product_crud'))



## Carga de Arvhivos DEL SISTEM INVENTARIO
@login_required
def cargar_inventario(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_excel = request.FILES['archivo_excel']
            df = pd.read_excel(archivo_excel)

            # Rellenar valores faltantes con 0 para columnas numéricas
            df['Código'] = df['Código'].fillna(0)
            df['Stock Actual'] = df['Stock Actual'].fillna(0)

            # Rellenar valores faltantes con None para columnas de texto
            df['Nombre (Princip.)'] = df['Nombre (Princip.)'].fillna(np.nan)
            df['Marca'] = df['Marca'].fillna(np.nan)
            df['Tip. Existencia'] = df['Tip. Existencia'].fillna(np.nan)

            for index, row in df.iterrows():
                codigo = row['Código']
                nombre = row['Nombre (Princip.)']
                marca = row['Marca']
                tipo_existencia = row['Tip. Existencia']
                stock_actual = row['Stock Actual']
                InventarioExcel.objects.create(
                    codigo=codigo,
                    nombre=nombre,
                    marca=marca,
                    tipo_existencia=tipo_existencia,
                    stock_actual=stock_actual
                )
            messages.success(request, '¡Datos cargados desde Excel!')
            return redirect('inventario:cargar_inventario')
    else:
        form = UploadFileForm()
    return render(request, 'cargar_inventario.html', {'form': form})

