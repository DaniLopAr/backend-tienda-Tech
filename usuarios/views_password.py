from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Usuario


import traceback


@api_view(['POST'])
def solicitar_reset(request):
    try:
        email = request.data.get('email')
        usuario = Usuario.objects.filter(email=email).first()
        if not usuario:
            return Response({'message': 'Correo enviado'})
        token = default_token_generator.make_token(usuario)
        uid = urlsafe_base64_encode(force_bytes(usuario.pk))

        link = f"https://front-tech-brown.vercel.app/reset-password/{uid}/{token}"

        send_mail(
            subject='Recuperación de contraseña - Techno',
            message=f'Hola {usuario.username},\n\nEnlace para restablecer tu contraseña:\n\n{link}\n\nEste enlace expira en 24 horas.',
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({'message': 'Correo enviado'})
    except Usuario.DoesNotExist:
        return Response({'message': 'Correo enviado'})
    except Exception as e:
        return Response({'error': str(e), 'trace': traceback.format_exc()}, status=500)


@api_view(['POST'])
def confirmar_reset(request):
    uid = request.data.get('uid')
    token = request.data.get('token')
    password = request.data.get('password')

    try:
        pk = force_str(urlsafe_base64_decode(uid))
        usuario = Usuario.objects.get(pk=pk)

        if default_token_generator.check_token(usuario, token):
            usuario.set_password(password)
            usuario.save()
            return Response({'message': 'Contraseña actualizada'})
        else:
            return Response({'error': 'Token inválido o expirado'}, status=400)
    except Exception:
        return Response({'error': 'Error al procesar la solicitud'}, status=400)
    
    from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_email(request):
    try:
        send_mail(
            subject='Test Brevo',
            message='Si recibes esto, Brevo funciona.',
            from_email=None,
            recipient_list=['dj02lopeza@gmail.com'],  # tu correo
            fail_silently=False,
        )
        return Response({'message': 'Correo enviado'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
