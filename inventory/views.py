from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Inventory
from products.models import Product

@staff_member_required
def manage_inventory(request):
    inventories = Inventory.objects.all()
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id=product_id)
        inventory, created = Inventory.objects.get_or_create(product=product)
        inventory.quantity = quantity
        inventory.save()
        return redirect('manage_inventory')
    return render(request, 'inventory/manage_inventory.html', {'inventories': inventories})