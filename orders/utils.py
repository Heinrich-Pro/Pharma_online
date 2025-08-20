# orders/utils.py
# Fonctions utilitaires pour la gestion des commandes
# Contient la logique de génération des factures PDF avec ReportLab

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import datetime


def generate_invoice_pdf(order):
    """
    Génère une facture PDF professionnelle pour une commande
    
    Cette fonction utilise ReportLab pour créer un PDF structuré contenant :
    1. En-tête avec le nom de la pharmacie
    2. Informations de la commande (numéro, date, client)
    3. Détail des articles commandés avec prix
    4. Total de la commande
    5. Instructions de récupération
    6. Pied de page
    
    Args:
        order (Order): L'objet commande pour lequel générer la facture
        
    Returns:
        bytes: Contenu binaire du PDF généré
        
    Utilisation typique :
    - Téléchargement par le client
    - Impression pour les archives
    - Envoi par email
    """
    # Création d'un buffer en mémoire pour stocker le PDF
    buffer = BytesIO()
    
    # Configuration du document avec format A4 (standard européen)
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # ===== CONFIGURATION DES STYLES =====
    
    # Récupération des styles par défaut de ReportLab
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour le titre principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,                    # Taille de police
        spaceAfter=30,                  # Espace après le titre
        textColor=colors.darkblue,      # Couleur du texte
        alignment=1                     # Centrage (1 = centre)
    )

    # ===== CONSTRUCTION DU CONTENU =====
    
    # Liste des éléments à ajouter au PDF
    story = []

    # En-tête principal avec le nom de la pharmacie
    story.append(Paragraph("PHARMACIE EN LIGNE", title_style))
    story.append(Spacer(1, 20))  # Espacement de 20 points

    # ===== INFORMATIONS DE LA COMMANDE =====
    
    # Tableau des informations de base de la commande
    order_info = [
        ['Numéro de commande:', order.order_number],
        ['Date:', order.created_at.strftime('%d/%m/%Y %H:%M')],
        ['Client:', f"{order.user.first_name} {order.user.last_name}"],
        ['Email:', order.user.email],
        ['Statut:', order.get_status_display()],
    ]

    # Création du tableau avec largeurs de colonnes personnalisées
    order_table = Table(order_info, colWidths=[2 * inch, 3 * inch])
    
    # Application du style au tableau des informations
    order_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),      # Police pour tout le tableau
        ('FONTSIZE', (0, 0), (-1, -1), 10),               # Taille de police
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),              # Alignement à droite pour les labels
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),               # Alignement à gauche pour les valeurs
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),  # Police en gras pour les labels
    ]))

    story.append(order_table)
    story.append(Spacer(1, 30))  # Espacement de 30 points

    # ===== DÉTAILS DES ARTICLES =====
    
    # Titre de section pour les détails
    story.append(Paragraph("Détails de la commande", styles['Heading2']))
    story.append(Spacer(1, 10))

    # En-tête du tableau des articles avec colonnes
    items_data = [['Médicament', 'Quantité', 'Prix unitaire', 'Total']]

    # Ajout de chaque article de la commande
    for item in order.items.all():
        items_data.append([
            item.medicine.name,                    # Nom du médicament
            str(item.quantity),                    # Quantité commandée
            f"{item.price}€",                     # Prix unitaire
            f"{item.total_price}€"                # Prix total pour cet article
        ])

    # Ligne de total général de la commande
    items_data.append(['', '', 'TOTAL:', f"{order.total_amount}€"])

    # Création du tableau des articles avec largeurs optimisées
    items_table = Table(items_data, colWidths=[3 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
    
    # Style élaboré pour le tableau des articles
    items_table.setStyle(TableStyle([
        # En-tête du tableau
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),     # Police en gras pour l'en-tête
        ('FONTSIZE', (0, 0), (-1, 0), 12),                   # Taille plus grande pour l'en-tête
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),         # Fond gris pour l'en-tête
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),   # Texte blanc pour l'en-tête
        
        # Alignement général
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),               # Centrage général
        ('ALIGN', (0, 1), (0, -2), 'LEFT'),                  # Alignement à gauche pour les noms de médicaments
        
        # Corps du tableau
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),         # Police normale pour le contenu
        ('FONTSIZE', (0, 1), (-1, -1), 10),                  # Taille normale pour le contenu
        
        # Bordures et grille
        ('GRID', (0, 0), (-1, -2), 1, colors.black),         # Grille pour les articles
        
        # Ligne de total
        ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),  # Police en gras pour le total
        ('FONTSIZE', (-2, -1), (-1, -1), 12),                # Taille plus grande pour le total
        ('BACKGROUND', (-2, -1), (-1, -1), colors.lightgrey), # Fond gris clair pour le total
    ]))

    story.append(items_table)
    story.append(Spacer(1, 30))

    # ===== INSTRUCTIONS DE RÉCUPÉRATION =====
    
    # Instructions importantes pour le client
    instructions = """
    <b>Instructions de récupération :</b><br/>
    • Présentez-vous à la pharmacie avec cette facture<br/>
    • Le paiement s'effectue lors de la récupération<br/>
    • Apportez une pièce d'identité valide<br/>
    • Pour les médicaments sur ordonnance, présentez votre ordonnance<br/>
    """

    story.append(Paragraph(instructions, styles['Normal']))
    story.append(Spacer(1, 20))

    # ===== PIED DE PAGE =====
    
    # Message de remerciement
    footer = "Merci de votre confiance ! - Pharmacie en ligne"
    story.append(Paragraph(footer, styles['Normal']))

    # ===== GÉNÉRATION FINALE =====
    
    # Construction du PDF avec tous les éléments
    doc.build(story)
    
    # Récupération du contenu binaire
    pdf = buffer.getvalue()
    
    # Fermeture du buffer pour libérer la mémoire
    buffer.close()

    return pdf
