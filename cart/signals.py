from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem
from shop.models import Product

 
   


@receiver(user_logged_in)
def merge_carts_on_login(sender, request, user, **kwargs):
    session_cart = request.session.get('cart')
    cart, created = Cart.objects.get_or_create(user=user)

    if session_cart:
        for product_id, item in session_cart.items():
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()

     
    new_session_cart = {}
    for item in cart.items.all():
        new_session_cart[str(item.product.id)] = {'quantity': item.quantity}

    request.session['cart'] = new_session_cart
    request.session.modified = True
