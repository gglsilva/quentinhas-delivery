from django.shortcuts import render

# Create your views here.
def Cardapio(request):
    template_name = 'produto/cardapio.html'
    return render(request, template_name)