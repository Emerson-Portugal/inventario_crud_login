# login/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse_lazy

# Create your views here.

@login_required
def home (request):
    return render(request, 'home.html')

@login_required
def products(request):
    return redirect(reverse_lazy('inventario:product_crud'))


@login_required
def cargarInventario(request):
    return redirect(reverse_lazy('inventario:cargar_inventario'))


def exit(request):
    logout(request)
    return redirect('home')