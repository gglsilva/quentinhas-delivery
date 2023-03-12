from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # path("", views.Home.as_view(), name="home"),
    path("", views.report_day, name="report-day"),
]