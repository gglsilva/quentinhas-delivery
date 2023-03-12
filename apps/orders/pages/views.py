from django.shortcuts import render
from ..models import Order, OrderItem
from ..forms import OrderCreateForm
from apps.cart.cart import Cart
from apps.orders.tasks import order_created


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