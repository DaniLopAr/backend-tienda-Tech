from django.db import models
from usuarios.models import Usuario
from productos.models import Producto

class Orden(models.Model):
    ESTADOS = [
        ('pendiente',  'Pendiente'),
        ('pagada',     'Pagada'),
        ('enviada',    'Enviada'),
        ('entregada',  'Entregada'),
    ]

    usuario  = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado   = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total    = models.DecimalField(max_digits=10, decimal_places=2)
    creada   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden {self.id} - {self.usuario}"

class OrdenItem(models.Model):
    orden    = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio   = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto} x{self.cantidad}"
    
    
    

