from django import forms
from .models import Order

# class OrderCreateForm(forms.ModelForm):
    
#     class Meta:
#         model = Order
#         fields = ['first_name', 'last_name', 'email', 'address',
#                      'postal_code', 'city']


# class OrderCreateForm(forms.ModelForm):

#     class Meta:
#         model = Order
#         fields = ['client','note']

    
        
class OrderCreateForm(forms.Form):
    cliente = forms.CharField(widget=forms.HiddenInput)
    Observação = forms.CharField(widget=forms.Textarea())
    
        