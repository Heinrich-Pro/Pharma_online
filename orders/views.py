from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import Product
from inventory.models import Inventory
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, status='pending')
    order_item, created = OrderItem.objects.get_or_create(
        order=order, product=product, defaults={'quantity': 1, 'price': product.price}
    )
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('cart')

@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, status='pending').first()
    return render(request, 'orders/cart.html', {'order': order})

@login_required
def confirm_order(request):
    order = Order.objects.filter(user=request.user, status='pending').first()
    if order:
        for item in order.items.all():
            inventory = Inventory.objects.get(product=item.product)
            if inventory.quantity < item.quantity:
                return render(request, 'orders/cart.html', {
                    'order': order,
                    'error': f"Stock insuffisant pour {item.product.name}"
                })
            inventory.quantity -= item.quantity
            inventory.save()
        order.status = 'confirmed'
        order.total_price = sum(item.get_total() for item in order.items.all())
        order.save()
        generate_invoice(order)
        return redirect('order_confirmation', order_id=order.id)
    return redirect('cart')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})

def generate_invoice(order):
    file_path = f"media/invoices/invoice_{order.id}.pdf"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"Facture pour la commande {order.id}", styles['Title']))
    elements.append(Paragraph(f"Client: {order.user.username}", styles['Normal']))
    elements.append(Paragraph(f"Date: {order.created_at}", styles['Normal']))

    data = [['Produit', 'Quantité', 'Prix unitaire', 'Total']]
    for item in order.items.all():
        data.append([item.product.name, item.quantity, f"{item.price} €", f"{item.get_total()} €"])
    data.append(['', '', 'Total', f"{order.total_price} €"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)