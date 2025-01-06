from django.conf import settings
from main.models import ClothingItem


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    
    def add(self, clothing_item, size, quantity=1):
        item_id = str(clothing_item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0, 'size': size}
        self.cart[item_id]['quantity'] = quantity
        self.save()


    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    
    def remove(self, clothing_item):
        item_id = str(clothing_item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    
    def get_total_price(self):
        total = 0
        for item_id, item_date in self.cart.items():
            try:
                clothing_item = ClothingItem.objects.get(id=item_id)
                total += clothing_item.get_price_with_discount() * item_date['quantity']
            except ClothingItem.DoesNotExist:
                continue
        return total
    

    def __iter__(self):
        item_ids = self.cart.keys()
        items = ClothingItem.objects.filter(id__in=item_ids)
        for item in items:
            total_price = item.get_price_with_discount()
            quantity = self.cart[str(item.id)]['quantity']
            yield {
                'item': item,
                'quantity': quantity,
                'size': self.cart[str(item.id)]['size'],
                'total_price': total_price * quantity,
            }
        
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
        