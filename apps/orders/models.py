from django.db import models
from apps.shop.models import Product
from apps.account.models import Profile

# Create your models here.
class Order(models.Model):
    client = models.ForeignKey(
        Profile,
        related_name='Cliente',
        on_delete=models.CASCADE
    )
    note = models.TextField(
        blank=True,
        null=True
    )
    created = models.DateField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    @property
    def get_product_for_order(self):
        return ''.join(f'{item.product.name}, ' for item in self.items.all())
    
    @property
    def return_note_with_string(self):
        return f'{self.note}' if self.note else ''


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2 
    )
    quantity = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    @property
    def get_produt_quantity(self):
        return f'{self.product.name} + {self.quantity}'
    