from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from ..models import Order, OrderItem
from ..forms import OrderCreateForm
from apps.cart.cart import Cart
from apps.shop.models import Product, Category
from apps.account.models import Profile
from ..utils import arrange_order, format_product_list
from datetime import date
# from django.template.loader import get_template
from django.template import Context

from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML
from django.contrib.auth.decorators import login_required



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

@login_required
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


def action_print_report_orders(request):
    today = date.today()
    orders = Order.objects.filter(created=date.today())
    html_string = render_to_string('core/pdf.html', {'orders': orders,
                                                     'today': today})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/relatorio.pdf')

    fs = FileSystemStorage('/tmp')

    with fs.open('relatorio.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    return response

def order_created(request):
    template_name = "orders/order/created.html"
    return render(request, template_name)