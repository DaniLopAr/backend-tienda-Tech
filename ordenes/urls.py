from django.urls import path
from .views import CreatePaymentIntentView, ConfirmarOrdenView
from .email import enviar_factura


urlpatterns = [
    path('create-payment-intent/', CreatePaymentIntentView.as_view()),
    path('confirmar/', ConfirmarOrdenView.as_view()),
]
