from django.core.mail import send_mail
from django.template.loader import render_to_string

def enviar_factura(email, nombre, items, total):
    cuerpo = f"""
    Hola {nombre}, gracias por tu compra en Techno.

    Resumen de tu pedido:
    """
    for item in items:
        cuerpo += f"\n- {item['nombre']} x{item['cantidad']} — ₡{item['precio']:,.0f}"
    
    cuerpo += f"\n\nTotal: ₡{total:,.0f}"
    cuerpo += "\n\nGracias por confiar en nosotros."

    send_mail(
        subject='Tu factura de Techno',
        message=cuerpo,
        from_email=None,  # usa DEFAULT_FROM_EMAIL
        recipient_list=[email],
        fail_silently=True,
    )