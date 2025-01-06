from django.db import models 


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)


    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.name
    

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    
    def get_item_count(self):
        return ClothingItem.objects.filter(category=self).count()


class ClothingItem(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    available = models.BooleanField(default=True)
    sizes = models.ManyToManyField(Size, through='ClothingItemSize',
                                   related_name='clothing_item', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 related_name='clothing_items')
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    

    def __str__(self):
        return self.name
    

    def get_price_with_discount(self):
        if self.discount > 0:
            return round(self.price * (1 - (self.discount / 100)), 2)
        return round(self.price, 2)
    

class ClothingItemSize(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)


    class Meta:
        unique_together = ('clothing_item', 'size')

    
class ItemImage(models.Model):
    product = models.ForeignKey(ClothingItem, related_name='images',
                                on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)

    
    def __str__(self):
        return f'{self.product.name} - {self.image.name}'
    