import os
import sib_api_v3_sdk
from datetime import datetime
import random

def enviar_factura(email, nombre, items, total):
    numero_orden = f"TEC-{random.randint(10000, 99999)}"
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    envio = "¡Gratis!" if total > 2000 else "₡15"

    cuerpo = f"Hola {nombre}, gracias por tu compra en Techno.\n\n"
    cuerpo += f"Orden: {numero_orden}\nFecha: {fecha}\n\n"
    cuerpo += "Detalle del pedido:\n"
    cuerpo += "-" * 40 + "\n"
    
    for item in items:
        cuerpo += f"{item['nombre']} x{item['cantidad']} — ₡{item['precio']:,.0f}\n"
    
    cuerpo += "-" * 40 + "\n"
    cuerpo += f"Envío: {envio}\n"
    cuerpo += f"Total: ₡{total:,.0f}\n\n"
    cuerpo += "Gracias por confiar en nosotros.\nEquipo Techno"

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    correo = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email}],
        sender={"email": "dj02lopeza@gmail.com", "name": "Techno"},
        subject=f"Tu factura {numero_orden} - Techno",
        text_content=cuerpo
    )

    try:
        api_instance.send_transac_email(correo)
    except Exception as e:
        print(f"Error enviando factura: {e}")
