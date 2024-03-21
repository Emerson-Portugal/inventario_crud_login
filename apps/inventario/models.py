# inventario/models.py
from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    codigo = models.CharField(primary_key=True, max_length=6)
    nombre = models.CharField(max_length=50)
    cantidad = models.PositiveSmallIntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class InventarioExcel(models.Model):
    codigo = models.CharField(max_length=500)
    nombre = models.CharField(max_length=500)
    marca = models.CharField(max_length=500)
    tipo_existencia = models.CharField(max_length=500)
    stock_actual = models.IntegerField()

    def __str__(self):
        return f'Código: {self.codigo}, Nombre: {self.nombre}'