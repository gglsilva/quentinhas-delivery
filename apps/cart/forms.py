from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    """
    Permite adicionar produtos ao carrinho
    Att:
        quantity: permite que o usuario seleciona a quantidade
                  entre 1 e 20, e converte a entrada para int.
        override: indique se a quantidade deve ser adicionada 
                  a qualquer quantidade existente no carrinho 
                  para este produto ou ser substituída pela 
                  quantidade fornecida.
    """
    quantity = forms.TypedChoiceField(label='Your name',
                                    choices=PRODUCT_QUANTITY_CHOICES,
                                    coerce=int)
    override = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)                      

class CardAddProductInlistForm(forms.Form):
    quantity = forms.IntegerField(max_value=2, min_value=0)
    override = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)