from django.db import models
from main.models import ClothingItem, Size
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    house_number = models.CharField(max_length=10)
    apartment_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    tracking_number = models.CharField(max_length=40, blank=True,
                                       default='Pending')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='pending')
    

    def __str__(self):
        return f'Order {self.id} from {self.first_name} {self.last_name}'
    

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',
                              on_delete=models.CASCADE)
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f'{self.quantity} x {self.clothing_item} ({self.size})'
    

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        