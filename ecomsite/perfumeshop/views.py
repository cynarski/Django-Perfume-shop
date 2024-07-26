from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Perfume, Order, OrderItem, ShippingAddress
import json
import datetime


def index(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

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

    context = {
        'perfumes': perfumes,
        'all_brands': all_brands,
        'filter_params': filter_params,
        'cartItems': cartItems,
        'user': request.user,  # Add this line
    }
    return render(request, 'perfumeshop/index.html', context)


def detail(request, id):
    product_object = Perfume.objects.get(id=id)
    return render(request, 'perfumeshop/detail.html', {'product_object': product_object})


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'perfumeshop/checkout.html', context)


def cart(request):
    if request.user.is_authenticated:

        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        # print(cart)
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

        for i in cart:
            try:
                # print(cart[i]['quantity'])
                cartItems += cart[i]['quantity']

                # print(Perfume.objects.get(id=i))
                product = Perfume.objects.get(id=i)
                total = product.price * cart[i]['quantity']

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                # print(order)

                item = {
                    'product': {
                        'id': product.id,
                        'name': product.brand + ' ' + product.name,
                        'price': product.price,
                        'image': product.image
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                # print(item, flush=True)
                items.append(item)

                if not product.digital:
                    order['shipping'] = True
            except:
                pass

    print(order, flush=True)
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'perfumeshop/cart.html', context)


@csrf_exempt
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Perfume.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.completed = True

        order.save()

    else:
        customer, order = guestOrder(request, data)

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
