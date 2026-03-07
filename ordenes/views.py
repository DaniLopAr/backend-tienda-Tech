import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .email import enviar_factura

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            amount = request.data.get('amount')
            items = request.data.get('items', [])
            nombre = request.data.get('nombre', 'Cliente')

            intent = stripe.PaymentIntent.create(
                amount=int(float(amount)),
                currency='crc',
            )

            # Guardar datos temporalmente en el intent para usarlos después
            return Response({
                'clientSecret': intent['client_secret'],
            })
        except Exception as e:
            print('Error:', str(e))
            return Response({'error': str(e)}, status=400)


class ConfirmarOrdenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            items = request.data.get('items', [])
            total = request.data.get('total', 0)
            nombre = request.data.get('nombre', 'Cliente')

            print('Enviando factura a:', request.user.email)
            print('Items:', items)
            print('Total:', total)

            resultado = enviar_factura(
                orden_data={
                    'nombre': nombre,
                    'items': items,
                    'total': total,
                },
                email_destino=request.user.email
            )

            print('Resultado envío:', resultado)
            return Response({'ok': True})
        except Exception as e:
            print('Error confirmando orden:', str(e))
            return Response({'error': str(e)}, status=400)
