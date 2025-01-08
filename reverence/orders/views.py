from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import OrderItem, Order
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from main.models import Size
from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


@login_required(login_url='/users/login')
def order_create(request):
    cart = Cart(request)
    total_price = sum(item['total_price'] for item in cart)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(
                user=request.user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                middle_name=form.cleaned_data.get('middle_name'),
                city=form.cleaned_data.get('city'),
                street=form.cleaned_data.get('street'),
                house_number=form.cleaned_data.get('house_number'),
                apartment_number=form.cleaned_data.get('apartment_number'),
                postal_code=form.cleaned_data.get('postal_code'),
            )
            order.save()

            for item in cart:
                size_instance = Size.objects.get(name=item['size'])
                OrderItem.objects.create(
                    order=order,
                    clothing_item=item['item'],
                    size=size_instance,
                    quantity=item['quantity'],
                    total_price=item['total_price'],
                )

            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {
                                    'name': item['item'].name,
                                },
                                'unit_amount': int(item['total_price'] * 100),
                            },
                            'quantity': item['quantity'],
                        } for item in cart 
                    ],
                    mode='payment',
                    success_url='http://localhost:8000/orders/completed',
                    cancel_url='http://localhost:8000/orders/create',
                )

                return redirect(session.url, code=303)
            except Exception as e:
                return render(request, 'orders/order_form.html', {
                    'form': form,
                    'cart': cart,
                    'error': str(e),
                })
            
    form = OrderForm(initial={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'middle_name': request.user.middle_name,
        'city': request.user.city,
        'street': request.user.street,
        'house_number': request.user.house_number,
        'apartment_number': request.user.apartment_number,
        'postal_code': request.user.postal_code,
    })

    return render(request, 'orders/order_form.html', {
        'form': form,
        'cart': cart,
        'total_price': total_price,
    })


@login_required(login_url='/users/login')
def order_success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'orders/order_success.html')
