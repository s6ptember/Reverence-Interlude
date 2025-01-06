from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from django.views import View
from main.models import ClothingItem, ClothingItemSize, \
    Size


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, item_id):
    cart = Cart(request)
    clothing_item = get_object_or_404(ClothingItem, id=item_id)
    size = request.POST.get('size')

    if size:
        try:
            size_obj = Size.objects.get(name=size)
            clothing_item_size = ClothingItemSize.objects.get(clothing_item=clothing_item,
                                                              size=size_obj)
            if not clothing_item_size.available:
                return redirect('cart:cart_detail')
        except Size.DoesNotExist:
            return redirect('cart:cart_detail')
        except ClothingItemSize.DoesNotExist:
            return redirect('cart:cart_detail')
    else:
        available_sizes = clothing_item.sizes.filter(clothingitemsize__available=True)
        if available_sizes.exists():
            size_obj = available_sizes.first()
            size = size_obj.name
        else:
            return redirect('cart:cart_detil')

    cart.add(clothing_item, size)
    return redirect('cart:cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    clothing_item = get_object_or_404(ClothingItem, id=item_id)
    cart.remove(clothing_item)
    return redirect('cart:cart_detail')


class CartUpdateView(View):
    def post(self, request, item_id):
        cart = Cart(request)
        quantity = request.POST.get('quantity', 1)
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
        clothing_item = get_object_or_404(ClothingItem, id=item_id)

        if quantity > 0:
            cart.add(clothing_item, cart.cart[str(item_id)]['size'], quantity)
        else:
            cart.remove(clothing_item)

        return redirect('cart:cart_detail')
    