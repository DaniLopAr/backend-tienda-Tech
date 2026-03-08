import os
import sib_api_v3_sdk

def enviar_factura(email, nombre, items, total):
    cuerpo = f"Hola {nombre}, gracias por tu compra en Techno.\n\nResumen de tu pedido:\n"
    
    for item in items:
        cuerpo += f"\n- {item['nombre']} x{item['cantidad']} — ₡{item['precio']:,.0f}"
    
    cuerpo += f"\n\nTotal: ₡{total:,.0f}"
    cuerpo += "\n\nGracias por confiar en nosotros.\n\nEquipo Techno"

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    correo = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email}],
        sender={"email": "dj02lopeza@gmail.com", "name": "Techno"},
        subject="Tu factura de Techno",
        text_content=cuerpo
    )
    
    try:
        api_instance.send_transac_email(correo)
    except Exception as e:
        print(f"Error enviando factura: {e}")