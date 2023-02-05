from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def dashboard(request):
    template_name = 'account/dashboard.html'
    return render(request, template_name, {'section':'dashboard'})