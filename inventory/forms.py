# inventory/forms.py
from django import forms
from .models import StockMovement
from products.models import Medicine


class StockUpdateForm(forms.Form):
    MOVEMENT_CHOICES = [
        ('in', 'Entrée de stock'),
        ('out', 'Sortie de stock'),
        ('adjustment', 'Ajustement'),
    ]

    movement_type = forms.ChoiceField(
        choices=MOVEMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    reason = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Motif de la modification"
    )


class StockMovementFilterForm(forms.Form):
    medicine = forms.ModelChoiceField(
        queryset=Medicine.objects.all(),
        required=False,
        empty_label="Tous les médicaments",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    movement_type = forms.ChoiceField(
        choices=[('', 'Tous les types')] + StockMovement.MOVEMENT_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


# Vues supplémentaires pour l'administration des produits
from products.forms import MedicineForm, CategoryForm


@staff_member_required
def manage_medicines(request):
    medicines = Medicine.objects.select_related('category').order_by('name')

    # Filtrage et recherche
    search_query = request.GET.get('search')
    if search_query:
        medicines = medicines.filter(name__icontains=search_query)

    category_filter = request.GET.get('category')
    if category_filter:
        medicines = medicines.filter(category_id=category_filter)

    # Pagination
    paginator = Paginator(medicines, 20)
    page_number = request.GET.get('page')
    medicines = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'medicines': medicines,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
    }

    return render(request, 'inventory/manage_medicines.html', context)


@staff_member_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            medicine = form.save()
            # Enregistrer le mouvement de stock initial
            if medicine.stock_quantity > 0:
                StockMovement.objects.create(
                    medicine=medicine,
                    movement_type='in',
                    quantity=medicine.stock_quantity,
                    reason='Stock initial',
                    created_by=request.user
                )
            messages.success(request, f"Médicament {medicine.name} ajouté avec succès!")
            return redirect('inventory:manage_medicines')
    else:
        form = MedicineForm()

    return render(request, 'inventory/add_medicine.html', {'form': form})


@staff_member_required
def edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    old_stock = medicine.stock_quantity

    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES, instance=medicine)
        if form.is_valid():
            updated_medicine = form.save()

            # Enregistrer le changement de stock si modifié
            if old_stock != updated_medicine.stock_quantity:
                quantity_diff = updated_medicine.stock_quantity - old_stock
                StockMovement.objects.create(
                    medicine=updated_medicine,
                    movement_type='adjustment',
                    quantity=quantity_diff,
                    reason='Modification manuelle',
                    created_by=request.user
                )

            messages.success(request, f"Médicament {updated_medicine.name} modifié avec succès!")
            return redirect('inventory:manage_medicines')
    else:
        form = MedicineForm(instance=medicine)

    context = {
        'form': form,
        'medicine': medicine,
    }

    return render(request, 'inventory/edit_medicine.html', context)


@staff_member_required
def manage_categories(request):
    categories = Category.objects.annotate(
        medicine_count=Count('medicines')
    ).order_by('name')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie ajoutée avec succès!")
            return redirect('inventory:manage_categories')
    else:
        form = CategoryForm()

    context = {
        'categories': categories,
        'form': form,
    }

    return render(request, 'inventory/manage_categories.html', context)