# orders/utils.py
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import datetime


def generate_invoice_pdf(order):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=1  # Center
    )

    # Contenu du PDF
    story = []

    # En-tête
    story.append(Paragraph("PHARMACIE EN LIGNE", title_style))
    story.append(Spacer(1, 20))

    # Informations de la commande
    order_info = [
        ['Numéro de commande:', order.order_number],
        ['Date:', order.created_at.strftime('%d/%m/%Y %H:%M')],
        ['Client:', f"{order.user.first_name} {order.user.last_name}"],
        ['Email:', order.user.email],
        ['Statut:', order.get_status_display()],
    ]

    order_table = Table(order_info, colWidths=[2 * inch, 3 * inch])
    order_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ]))

    story.append(order_table)
    story.append(Spacer(1, 30))

    # Détails des articles
    story.append(Paragraph("Détails de la commande", styles['Heading2']))
    story.append(Spacer(1, 10))

    # En-tête du tableau des articles
    items_data = [['Médicament', 'Quantité', 'Prix unitaire', 'Total']]

    for item in order.items.all():
        items_data.append([
            item.medicine.name,
            str(item.quantity),
            f"{item.price}€",
            f"{item.total_price}€"
        ])

    # Ligne de total
    items_data.append(['', '', 'TOTAL:', f"{order.total_amount}€"])

    items_table = Table(items_data, colWidths=[3 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
    items_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -2), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -2), 1, colors.black),
        ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (-2, -1), (-1, -1), 12),
        ('BACKGROUND', (-2, -1), (-1, -1), colors.lightgrey),
    ]))

    story.append(items_table)
    story.append(Spacer(1, 30))

    # Instructions
    instructions = """
    <b>Instructions de récupération :</b><br/>
    • Présentez-vous à la pharmacie avec cette facture<br/>
    • Le paiement s'effectue lors de la récupération<br/>
    • Apportez une pièce d'identité valide<br/>
    • Pour les médicaments sur ordonnance, présentez votre ordonnance<br/>
    """

    story.append(Paragraph(instructions, styles['Normal']))
    story.append(Spacer(1, 20))

    # Pied de page
    footer = "Merci de votre confiance ! - Pharmacie en ligne"
    story.append(Paragraph(footer, styles['Normal']))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()

    return pdf
