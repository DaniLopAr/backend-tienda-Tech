from django.contrib import admin
from .models import Orden, OrdenItem


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'estado', 'total', 'creada']


@admin.register(OrdenItem)
class OrdenItemAdmin(admin.ModelAdmin):
    list_display = ['orden', 'producto', 'cantidad', 'precio']
