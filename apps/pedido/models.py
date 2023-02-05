from django.db import models
from apps.account.models import Profile
from apps.produto.models import Produto

# Create your models here.
class Pedido(models.Model):
    usuario = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    observacao = models.TextField()
    data = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.usuario.user.username

class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE
    )
    quantidade = models.IntegerField()
