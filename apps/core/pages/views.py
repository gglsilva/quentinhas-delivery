from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView
from datetime import date
from apps.orders.models import Order
from PIL import Image
import pytesseract
from django.contrib.auth.decorators import login_required
from apps.account.models import Profile
from django.contrib.auth.models import User


@login_required
class Home(TemplateView):
    template_name = "core/index.html"


@login_required
def report_day(request):
    # template_name = "core/index.html"
    template_name = "core/dashboard.html"
    user = request.user
    profile = Profile.objects.get(user__username=user)
    orders = Order.objects.all()
    context = {
        'orders': orders,
        'profile': profile.is_admin,
    }
    return render(request, template_name, context)




# def extract_productd_image(request):
#     if request.method == 'POST':
#         imagem = request.FILES['imagem']
    # imagem = Image.open()
    # texto = pytesseract.image_to_string(imagem)

    # print(texto)
    # with open('texto_extraido.txt', 'w') as arquivo:
    #     arquivo.write(texto)   