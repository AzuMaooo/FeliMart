from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    new_quantity = int(request.POST.get('quantity'))

    if product_id_str in cart:
        cart[product_id_str] += new_quantity
        
    else:
        cart[product_id_str] = new_quantity

    request.session['cart'] = cart
    messages.success(request, f'Added {new_quantity}x {product.name} to cart!')
    return redirect('product_list')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session['cart'] = cart
    return redirect('view_cart')

def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))

        if new_quantity <= 0:
            if product_id_str in cart:
                del cart[product_id_str]
        else:
            cart[product_id_str] = new_quantity

        request.session['cart'] = cart

    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id_str, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str))
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('view_cart')

    order = Order.objects.create(user=request.user, total_price=0)

    order_total = 0
    for product_id_str, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str))
        line_total = product.price * quantity
        order_total += line_total

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            total_price=line_total
        )

    order.total_price = order_total
    order.save()

    request.session['cart'] = {}

    messages.success(request, f'Order #{order.id} placed successfully!')
    return redirect('view_cart')