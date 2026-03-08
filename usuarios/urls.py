from django.urls import path
from .views import RegistroView
from .views_password import solicitar_reset, confirmar_reset


urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('solicitar-reset/', solicitar_reset),
    path('confirmar-reset/', confirmar_reset),
]
