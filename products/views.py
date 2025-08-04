from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')

    if category_id:
        products = products.filter(category_id=category_id)
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
    })