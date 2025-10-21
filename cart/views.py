from django.shortcuts import render,get_object_or_404,redirect
from shop.models import Product,Order,OrderItem
from .models import Cart, CartItem


from django.contrib.auth.decorators import login_required

# Create your views here.
 


def _get_session_cart(request):
    return request.session.get('cart', {})


def _save_session_cart(request, cart_data):
    request.session['cart'] = cart_data
    request.session.modified = True


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_data = _get_session_cart(request)

    if str(product_id) in cart_data:
        cart_data[str(product_id)]['quantity'] += 1
    else:
        cart_data[str(product_id)] = {'quantity': 1}

    _save_session_cart(request, cart_data)

    
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:view_cart')


def remove_from_cart(request, product_id):
    cart_data = _get_session_cart(request)
    if str(product_id) in cart_data:
        del cart_data[str(product_id)]
    _save_session_cart(request, cart_data)

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()

    return redirect('cart:view_cart')


def view_cart(request):
    cart_items = []
    total = 0
    cart_=[]
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        for item in cart.items.select_related('product'):
            total += item.product.price * item.quantity
        cart_items = cart.items.all()
        cart_.append(cart)
        
    else:
        cart_data = _get_session_cart(request)
        for p_id, item in cart_data.items():
            product = get_object_or_404(Product, id=p_id)
            quantity = item['quantity']
            
            total += product.price * quantity
            
            cart_items.append({'product': product, 'quantity': quantity})

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total,'cart_':cart_})



def decrease_cart_item(request, product_id):
    cart_data = _get_session_cart(request)

    if str(product_id) in cart_data:
        if cart_data[str(product_id)]['quantity'] > 1:
            cart_data[str(product_id)]['quantity'] -= 1
        else:
            del cart_data[str(product_id)]  

        _save_session_cart(request,cart_data)

    if request.user.is_authenticated:
        
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        

    return redirect('cart:view_cart')
  

def checkout(request,cart_id):
    total=0
    
    cart=Cart.objects.get(id=cart_id)
    product=CartItem.objects.filter(cart_id=cart)
    for item in product:
         total+=item.product.price*item.quantity
          
         
    if request.method=="POST":
              
              name=request.POST.get("name","")
              email=request.POST.get("email","")
              address=request.POST.get("address","")
              city=request.POST.get("city","")
              state=request.POST.get("state","")
              zipcode=request.POST.get("zipcode","")
          
              order=Order(user=request.user,name=name,email=email,address=address,city=city,state=state,zipcode=zipcode)
        
              order.save()


              for item in product:
                   order_item=OrderItem(order=order,product=item.product,quantity=item.quantity,price=item.product.price) 
                 
                   order_item.save()
                   product.delete()   
                    
              return redirect('cart:order_placed')
    return render(request,'cart/checkout.html',{'product':product,'total':total})


def order_placed(request):
    return render(request,"cart/order_placed.html")
 
 


@login_required(login_url='accounts:login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items')  # or your related_name
    context = {
        'orders': orders,
    }
    return render(request, 'cart/order_history.html', context)



def cancel_order(request,id):
    order=Order.objects.filter(id=id).delete()
    return redirect('cart:order_history')

def  cancel_confirmation(request,id):
    orders=Order.objects.filter(id=id)
    return render(request,'cart/cancel_confirmation.html',{'orders':orders}) 