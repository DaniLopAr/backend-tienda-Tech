import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY


def enviar_factura(orden_data, email_destino):
    items_html = ""
    for item in orden_data['items']:
        items_html += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #2d2d3d;">{item['nombre']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #2d2d3d; text-align:center;">{item['cantidad']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #2d2d3d; text-align:right;">₡{item['precio']:,}</td>
            </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0; padding:0; background:#0a0a0f; font-family:'Helvetica Neue', sans-serif;">
        <div style="max-width:600px; margin:0 auto; padding:40px 20px;">
            <div style="text-align:center; margin-bottom:40px;">
                <h1 style="font-size:28px; font-weight:900; letter-spacing:4px; color:white; margin:0;">TECHSTORE</h1>
                <p style="color:#6b7280; font-size:12px; letter-spacing:2px; text-transform:uppercase; margin-top:8px;">Comprobante de compra</p>
            </div>
            <div style="background:#13111e; border:1px solid #2d2d3d; border-radius:20px; overflow:hidden;">
                <div style="background:#7c3aed22; padding:24px 32px; border-bottom:1px solid #2d2d3d;">
                    <p style="color:#a78bfa; font-size:11px; letter-spacing:3px; text-transform:uppercase; margin:0 0 6px;">¡Pago exitoso!</p>
                    <h2 style="color:white; font-size:22px; font-weight:700; margin:0;">Gracias por tu compra, {orden_data['nombre']} 🎉</h2>
                </div>
                <div style="padding:32px;">
                    <table style="width:100%; border-collapse:collapse; margin-bottom:24px;">
                        <thead>
                            <tr style="border-bottom:1px solid #2d2d3d;">
                                <th style="padding:10px; text-align:left; color:#6b7280; font-size:11px; letter-spacing:2px; text-transform:uppercase;">Producto</th>
                                <th style="padding:10px; text-align:center; color:#6b7280; font-size:11px; letter-spacing:2px; text-transform:uppercase;">Cant.</th>
                                <th style="padding:10px; text-align:right; color:#6b7280; font-size:11px; letter-spacing:2px; text-transform:uppercase;">Precio</th>
                            </tr>
                        </thead>
                        <tbody style="color:#e2e8f0; font-size:14px;">
                            {items_html}
                        </tbody>
                    </table>
                    <div style="background:#0a0a0f; border-radius:12px; padding:16px 20px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="color:#6b7280; font-size:13px; text-transform:uppercase; letter-spacing:2px;">Total pagado</span>
                            <span style="font-size:22px; font-weight:700; color:#a855f7;">₡{orden_data['total']:,}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div style="text-align:center; margin-top:32px;">
                <p style="color:#374151; font-size:12px;">© 2025 TechStore. San José, Costa Rica.</p>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": email_destino,
            "subject": "🛒 Tu factura de TechStore",
            "html": html_content,
        })
        return True
    except Exception as e:
        print('Error enviando correo:', str(e))
        return False
