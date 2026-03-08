from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Usuario
import os
import sib_api_v3_sdk


def enviar_correo(destinatario, asunto, contenido):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration))
    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": destinatario}],
        sender={"email": "dj02lopeza@gmail.com", "name": "Tech"},        subject=asunto,
        text_content=contenido
    )
    api_instance.send_transac_email(email)


@api_view(['GET'])
def test_email(request):
    try:
        enviar_correo('dj02lopeza@gmail.com', 'Test Brevo',
                      'Si recibes esto, Brevo funciona.')
        return Response({'message': 'Correo enviado'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


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

        enviar_correo(
            email,
            'Recuperación de contraseña - Techno',
            f'Hola {usuario.username},\n\nHaz click en el siguiente enlace para restablecer tu contraseña:\n\n{link}\n\nEste enlace expira en 24 horas.'
        )
        return Response({'message': 'Correo enviado'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def confirmar_reset(request):
    uid = request.data.get('uid')
    token = request.data.get('token')
    password = request.data.get('password')

    try:
        pk = force_str(urlsafe_base64_decode(uid))
        usuario = Usuario.objects.get(pk=pk)
        valid = default_token_generator.check_token(usuario, token)
        return Response({
            'usuario': usuario.username,
            'pk': pk,
            'valid': valid,
            'token': token,
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)
