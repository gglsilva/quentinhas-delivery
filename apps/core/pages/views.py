from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView
from datetime import date
from apps.orders.models import Order

# Create your views here.
class Home(TemplateView):
    template_name = "core/index.html"

def report_day(request):
    template_name = "core/index.html"
    orders = Order.objects.all()
    context = {
        'orders': orders
    }
    return render(request, template_name, context)