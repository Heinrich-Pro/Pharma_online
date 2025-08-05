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