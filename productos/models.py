from django.db import models
from cloudinary.models import CloudinaryField

class Producto(models.Model):
    CATEGORIAS = [
        ('Laptops',     'Laptops'),
        ('Smartphones', 'Smartphones'),
        ('Audio',       'Audio'),
        ('Wearables',   'Wearables'),
        ('Monitores',   'Monitores'),
        ('Gaming',      'Gaming'),
    ]

    nombre      = models.CharField(max_length=200)
    categoria   = models.CharField(max_length=100, choices=CATEGORIAS)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    imagen      = CloudinaryField('imagen', blank=True, null=True)
    emoji       = models.CharField(max_length=10, blank=True)
    badge       = models.CharField(max_length=50, blank=True)
    rating      = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    reviews     = models.IntegerField(default=0)
    stock       = models.IntegerField(default=0)
    creado      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre