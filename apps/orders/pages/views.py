from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from ..models import Order, OrderItem
from ..forms import OrderCreateForm
from apps.cart.cart import Cart
from apps.shop.models import Product, Category
from apps.account.models import Profile
from ..utils import arrange_order, format_product_list
from datetime import date
from django.template.loader import get_template
from django.template import Context
from reportlab.pdfgen import canvas

def order_create(request):
    cart = Cart(request)
    user = request.user
    
    print(user)
    if request.method == 'POST':
        if request.user.is_authenticated:
            order = Order.objects.create(client=user.profile,
                                        note=request.POST.get('Observerção'))
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', 
                           {'cart':cart, 'form': form})                        

def new_order(request, category_slug=None):
    categories = Category.objects.all()
    acompanhamento = Product.objects.filter(available=True, category=categories[0])
    opcao = Product.objects.filter(available=True, category=categories[1])
    profiles = Profile.objects.all()

    context = {
        'opcoes': opcao,
        'acompanhamentos': acompanhamento,
        'profiles': profiles,
    }
        
    return render(request, 'orders/order/new.html', context)


def action_ajax_create_order(request):
    if request.method != 'POST':
        return HttpResponseServerError()
    quentinha = request.POST.getlist('produtos[]', None)
    cliente = request.POST.getlist('cliente', None)
    msg = request.POST.getlist('msg')
    cart = arrange_order(quentinha)
    client = Profile.objects.get(user__username=cliente[0])
    order = Order.objects.create(client=client,
                                    note=msg)
    price = 1
    quantity = 1
    for item in cart:
        produto = Product.objects.get(id=int(item))
        OrderItem.objects.create(order=order,
                                 product=produto,
                                 price=price,
                                 quantity=quantity)

    return HttpResponse("success!")


def action_print_report_orders(report):
    orders = Order.objects.all().filter(created=date.today())
    with open('pedidos.txt', 'w') as pd:
        for order in orders:
            list_product = format_product_list(order.get_product_for_order)
            # pd.writelines(f'{order.client} - {order.get_product_for_order} - {order.note} \n')
            pd.writelines(f'{order.client} - {list_product} - {order.note} \n')
        response = pd

    return response