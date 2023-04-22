from django import template
from apps.orders.models import Order
from datetime import date, timedelta

register = template.Library()

@register.simple_tag
def total_order():
    return Order.objects.count() 


@register.simple_tag
def total_order_today():
    return Order.objects.filter(created=date.today()).count()

@register.simple_tag
def total_mean_order():
    return Order.objects.filter(created__gte=date.today() - timedelta(days=7)).count()