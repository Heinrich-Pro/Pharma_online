<<<<<<< HEAD
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
=======
# orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Order, OrderItem, Cart, CartItem
from .utils import generate_invoice_pdf


@login_required
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart_items = []
        cart = None

    context = {
        'cart_items': cart_items,
        'cart': cart,
    }
    return render(request, 'orders/cart.html', context)


@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increase':
            if cart_item.quantity < cart_item.medicine.stock_quantity:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.warning(request, "Stock insuffisant.")

        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
                messages.info(request, "Article retiré du panier.")

        elif action == 'remove':
            cart_item.delete()
            messages.success(request, "Article retiré du panier.")

    return redirect('orders:cart')


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        messages.error(request, "Votre panier est vide.")
        return redirect('products:medicine_list')

    if not cart_items:
        messages.error(request, "Votre panier est vide.")
        return redirect('products:medicine_list')

    if request.method == 'POST':
        # Créer la commande
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_amount,
            notes=request.POST.get('notes', '')
        )

        # Créer les éléments de commande
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                medicine=cart_item.medicine,
                quantity=cart_item.quantity,
                price=cart_item.medicine.price
            )

            # Réduire le stock
            medicine = cart_item.medicine
            medicine.stock_quantity -= cart_item.quantity
            medicine.save()

        # Vider le panier
        cart.delete()

        messages.success(request, f"Commande {order.order_number} créée avec succès!")
        return redirect('orders:order_detail', pk=order.pk)

    context = {
        'cart_items': cart_items,
        'cart': cart,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{order.order_number}.pdf"'

    pdf = generate_invoice_pdf(order)
    response.write(pdf)

    return response


# Administration des commandes (pour le staff)
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')

    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'selected_status': status_filter,
    }
    return render(request, 'orders/admin_orders.html', context)


@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Statut de la commande {order.order_number} mis à jour.")

    return redirect('orders:admin_orders')
>>>>>>> develop
