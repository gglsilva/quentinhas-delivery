from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.models import User
from ..models import Order, OrderItem
from ..forms import OrderCreateForm
from apps.cart.cart import Cart
from apps.shop.models import Product, Category
from apps.account.models import Profile
from apps.orders.tasks import order_created
from ..utils import arrange_order
from datetime import date

# Create your views here.
# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for item in cart:
#                 OrderItem.objects.create(order=order,
#                                          product=item['product'],
#                                          price=item['price'],
#                                          quantity=item['quantity'])
#             # clear the cart
#             cart.clear()
#             # launch asynchronous taks
#             order_created.delay(order.id)
#             return render(request,
#                           'orders/order/created.html',
#                           {'order': order})
#     else:
#         form = OrderCreateForm()
#     return render(request, 'orders/order/create.html', 
#                            {'cart':cart, 'form': form})


def order_create(request):
    cart = Cart(request)
    user = request.user
    
    print(user)
    if request.method == 'POST':
        if request.user.is_authenticated:
            # order['client'] = user
            # order['node'] = request.POST.get('note')
            order = Order.objects.create(client=user.profile,
                                        note=request.POST.get('Observerção'))
        # if form.is_valid():
            # order = form.save()
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
    # print('\n ####')
    # print(request.user.profile)
    # print('\n ####')
    # if request.method == 'POST':
    #     print('\n ####')
    #     print(request.user)
    #     print('\n ####')
    # cart = Cart(request)
    # if request.method == 'POST':
    #     form = OrderCreateForm(request.POST)
    #     if form.is_valid():
    #         order = form.save()
    #         for item in cart:
    #             OrderItem.objects.create(order=order,
    #                                      product=item['product'],
    #                                      price=item['price'],
    #                                      quantity=item['quantity'])
    #         # clear the cart
    #         cart.clear()
    #         # launch asynchronous taks
    #         # order_created.delay(order.id)
    #         return render(request,
    #                       'orders/order/created2.html',
    #                       {'order': order})
    # else:
    #     form = OrderCreateForm()
    # return render(request, 'orders/order/create2.html', 
    #                        {'cart':cart, 'form': form})                        

def new_order(request, category_slug=None):
    categories = Category.objects.all()
    acompanhamento = Product.objects.filter(available=True, category=categories[0])
    opcao = Product.objects.filter(available=True, category=categories[1])
    profiles = Profile.objects.all()
        
    # if request.method == 'POST':
    #     quentinha = request.POST.getlist('produtos[]', None) 
    #     cliente = request.POST.getlist('cliente', None) 
    #     msg = request.POST.getlist('msg')
    #     # print(type(quentinha))
    #     # print(quentinha)
    #     # print(cliente)
    #     # print(msg)
    #     cart = arrange_order(quentinha)
        
    #     # me = User.objects.get(username=cliente[0])
    #     client = Profile.objects.get(user__username=cliente[0])

    #     order = Order.objects.create(client=client,
    #                                     note=msg)
    #     order_item = OrderItem()
    #     price = 1
    #     quantity = 1
    #     # print('>>>', cart[0])
    #     # print('>>>',Product.objects.filter(slug__contains=cart[0]))
    #     for item in cart:
    #     #     # print('>>>', item)
    #     #     order_item.add_item_in_order(
    #     #         order, item, price, quantity
    #     #     )
    #         produto = Product.objects.get(slug__contains=item)
    #         # print('>>>', produto)
    #         OrderItem.objects.create(order=order,
    #                                  product=produto,
    #                                  price=price,
    #                                  quantity=quantity)

    #     # for item in quentinha:
    #     #     print(item)
    #     # produto = Product.objects.filter(name__icontains=cart[0])
    #     # print('>>>', produto)
    #     # return redirect('orders/order/created.html',
    #     #                 {'order': order})
    #     return HttpResponse("Success!")
    # else:
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
    # print(quentinha)
    cart = arrange_order(quentinha)
    client = Profile.objects.get(user__username=cliente[0])
    order = Order.objects.create(client=client,
                                    note=msg)
    price = 1
    quantity = 1
    for item in cart:
        # produto = Product.objects.filter(slug__contains=item)
        # print(f'{item} - {type(item)}')
        produto = Product.objects.get(id=int(item))
        # print(type(produto))
        OrderItem.objects.create(order=order,
                                 product=produto,
                                 price=price,
                                 quantity=quantity)

    return HttpResponse("success!")


def action_print_report_orders(request):
    orders = Order.objects.all().filter(created=date.today())
    with open('pedidos.txt', 'w') as pd:
        for order in orders:
            pd.writelines(f'{order.client} - {order.get_product_for_order} - {order.note} \n')

    return HttpResponse()