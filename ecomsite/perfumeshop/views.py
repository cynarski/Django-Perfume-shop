from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from django.db import connection
from django.http import JsonResponse
from .models import Perfume, Order
import json

def index(request):
    perfumes = Perfume.objects.all().order_by()

    # get brands
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT brand FROM perfumeshop_perfume ORDER BY brand;")
        all_brands = [row[0] for row in cursor.fetchall()]

    # search code
    item_name = request.GET.get('item_name', '').strip()

    if item_name:
        perfumes = perfumes.filter(name__icontains=item_name) | perfumes.filter(brand__icontains=item_name)

    # price selector code
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    if min_price:
        try:
            min_price = float(min_price)
            perfumes = perfumes.filter(price__gte=min_price)
        except ValueError: 
            pass

    if max_price:
        try:
            max_price = float(max_price)
            perfumes = perfumes.filter(price__lte=max_price)
        except ValueError:
            pass

    # Brand filter code
    selected_brand = request.GET.get('brands')
    if selected_brand:
        perfumes = perfumes.filter(brand=selected_brand)

    # pagination code
    paginator = Paginator(perfumes, 12)
    page = request.GET.get('page')

    try:
        perfumes = paginator.page(page)
    except PageNotAnInteger:
        perfumes = paginator.page(1)
    except EmptyPage:
        perfumes = paginator.page(paginator.num_pages)

    # Collecting filter parameters
    filter_params = {
        'item_name': item_name,
        'min_price': min_price,
        'max_price': max_price,
        'brands': selected_brand,
    }

    return render(request, 'perfumeshop/index.html', {
        'perfumes': perfumes,
        'all_brands': all_brands,
        'filter_params': filter_params,
    })
def detail(request, id):
    
    product_object = Perfume.objects.get(id=id)
    return render(request, 'perfumeshop/detail.html', {'product_object': product_object})

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'perfumeshop/checkout.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'perfumeshop/cart.html', context)