from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name="order_create"),
    path('new-order/', views.new_order, name="new_order"), 
    path('order/create-ajax/', views.action_ajax_create_order, name="action_ajax_create_order"), 
    path("order/created/", views.order_created, name="order_created"),
    path('report/day/', views.action_print_report_orders, name="action_print_report_orders"), 
]