# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Medicine, Category
from orders.models import Cart, CartItem


def medicine_list(request):
    medicines = Medicine.objects.filter(is_available=True, stock_quantity__gt=0)
    categories = Category.objects.all()

    # Filtrage par catégorie
    category_id = request.GET.get('category')
    if category_id:
        medicines = medicines.filter(category_id=category_id)

    # Recherche
    search_query = request.GET.get('search')
    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(active_ingredient__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(medicines, 12)
    page_number = request.GET.get('page')
    medicines = paginator.get_page(page_number)

    context = {
        'medicines': medicines,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'products/medicine_list.html', context)


def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk, is_available=True)
    return render(request, 'products/medicine_detail.html', {'medicine': medicine})


@login_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id, is_available=True)

    if medicine.stock_quantity <= 0:
        messages.error(request, "Ce médicament n'est plus en stock.")
        return redirect('products:medicine_detail', pk=medicine_id)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        medicine=medicine,
        defaults={'quantity': 1}
    )

    if not created:
        if cart_item.quantity < medicine.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"{medicine.name} ajouté au panier.")
        else:
            messages.warning(request, "Stock insuffisant pour augmenter la quantité.")
    else:
        messages.success(request, f"{medicine.name} ajouté au panier.")

    return redirect('products:medicine_detail', pk=medicine_id)