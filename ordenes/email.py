import os
import base64
import random
import sib_api_v3_sdk
from io import BytesIO
from datetime import datetime
from django.template.loader import render_to_string
from xhtml2pdf import pisa


def enviar_factura(email, nombre, items, total):
    numero_orden = f"TEC-{random.randint(10000, 99999)}"
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    envio = "¡Gratis!" if total > 2000 else "₡15"

    items_detalle = []
    for item in items:
        precio_unitario = item['precio'] / \
            item['cantidad'] if item['cantidad'] > 0 else item['precio']
        items_detalle.append({
            'nombre': item['nombre'],
            'cantidad': item['cantidad'],
            'precio_unitario': precio_unitario,
            'subtotal': item['precio'],
        })

    html_string = render_to_string('factura.html', {
        'numero_orden': numero_orden,
        'fecha': fecha,
        'nombre': nombre,
        'items': items_detalle,
        'envio': envio,
        'total': total,
    })

    pdf_buffer = BytesIO()
    pisa.CreatePDF(html_string, dest=pdf_buffer)
    pdf = pdf_buffer.getvalue()

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration))

    correo = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email}],
        sender={"email": "dj02lopeza@gmail.com", "name": "Techno"},
        subject=f"Tu factura {numero_orden} - Techno",
        text_content=f"Hola {nombre}, adjuntamos tu factura de compra en Techno.\n\nGracias por tu compra.",
        attachment=[{
            "content": base64.b64encode(pdf).decode(),
            "name": f"factura-{numero_orden}.pdf"
        }]
    )

    try:
        api_instance.send_transac_email(correo)
    except Exception as e:
        print(f"Error enviando factura: {e}")
