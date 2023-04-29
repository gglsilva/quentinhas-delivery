from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # path("", views.Home.as_view(), name="home"),
    path("", views.report_day, name="report_day"),
    
    # path("get-text/", views.extract_productd_image, name="extract_productd_image"),
]