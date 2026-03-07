from django.contrib import admin
from .models import CarritoItem


@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'producto', 'cantidad']
