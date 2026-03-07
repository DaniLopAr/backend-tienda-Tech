from django.db import models
from usuarios.models import Usuario
from productos.models import Producto


class CarritoItem(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.usuario} - {self.producto}"



