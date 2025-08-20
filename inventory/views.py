# inventory/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import F, Sum, Count
from django.core.paginator import Paginator
from .models import StockMovement
from products.models import Medicine, Category
from .utils import update_stock, get_low_stock_medicines, get_out_of_stock_medicines
from .forms import StockUpdateForm, StockMovementFilterForm


@staff_member_required
def inventory_dashboard(request):
    # Statistiques générales
    total_medicines = Medicine.objects.count()
    total_categories = Category.objects.count()
    low_stock_count = get_low_stock_medicines().count()
    out_of_stock_count = get_out_of_stock_medicines().count()

    # Valeur totale du stock
    total_stock_value = Medicine.objects.aggregate(
        total=Sum(F('stock_quantity') * F('price'))
    )['total'] or 0

    # Médicaments les plus vendus (basé sur les mouvements de sortie)
    popular_medicines = Medicine.objects.annotate(
        sold_quantity=Sum('stock_movements__quantity',
                          filter=F('stock_movements__movement_type') == 'out')
    ).order_by('-sold_quantity')[:5]

    # Mouvements récents
    recent_movements = StockMovement.objects.select_related(
        'medicine', 'created_by'
    ).order_by('-created_at')[:10]

    context = {
        'total_medicines': total_medicines,
        'total_categories': total_categories,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'total_stock_value': total_stock_value,
        'popular_medicines': popular_medicines,
        'recent_movements': recent_movements,
    }

    return render(request, 'inventory/dashboard.html', context)


@staff_member_required
def stock_movements(request):
    movements = StockMovement.objects.select_related(
        'medicine', 'created_by'
    ).order_by('-created_at')

    # Filtrage
    form = StockMovementFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['medicine']:
            movements = movements.filter(medicine=form.cleaned_data['medicine'])
        if form.cleaned_data['movement_type']:
            movements = movements.filter(movement_type=form.cleaned_data['movement_type'])
        if form.cleaned_data['date_from']:
            movements = movements.filter(created_at__date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data['date_to']:
            movements = movements.filter(created_at__date__lte=form.cleaned_data['date_to'])

    # Pagination
    paginator = Paginator(movements, 25)
    page_number = request.GET.get('page')
    movements = paginator.get_page(page_number)

    context = {
        'movements': movements,
        'form': form,
    }

    return render(request, 'inventory/stock_movements.html', context)


@staff_member_required
def low_stock_report(request):
    low_stock_medicines = get_low_stock_medicines().select_related('category')
    out_of_stock_medicines = get_out_of_stock_medicines().select_related('category')

    context = {
        'low_stock_medicines': low_stock_medicines,
        'out_of_stock_medicines': out_of_stock_medicines,
    }

    return render(request, 'inventory/low_stock_report.html', context)


@staff_member_required
def update_stock_view(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)

    if request.method == 'POST':
        form = StockUpdateForm(request.POST)
        if form.is_valid():
            movement_type = form.cleaned_data['movement_type']
            quantity = form.cleaned_data['quantity']
            reason = form.cleaned_data['reason']

            try:
                update_stock(medicine, quantity, movement_type, reason, request.user)
                messages.success(
                    request,
                    f"Stock mis à jour pour {medicine.name}. Nouveau stock: {medicine.stock_quantity}"
                )
                return redirect('inventory:dashboard')
            except Exception as e:
                messages.error(request, f"Erreur lors de la mise à jour: {str(e)}")
    else:
        form = StockUpdateForm()

    context = {
        'form': form,
        'medicine': medicine,
    }

    return render(request, 'inventory/update_stock.html', context)