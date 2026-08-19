from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, AdvisorHistory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import paypalrestsdk
import anthropic
from django.conf import settings

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

    return redirect('order_confirm', order_id=order.id)

@login_required
def order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    return render(request, 'store/order_confirm.html', {'order': order, 'order_items': order_items})

@login_required
def paypal_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(f'/paypal/success/{order.id}/'),
            "cancel_url": request.build_absolute_uri(f'/paypal/cancel/{order.id}/'),
        },
        "transactions": [{
            "item_list": {
                "items": [
                    {
                        "name": item.product.name,
                        "sku": str(item.product.id),
                        "price": str(item.product.price),
                        "currency": "USD",
                        "quantity": item.quantity
                    } for item in order.items.all()
                ]
            },
            "amount": {
                "total": str(order.total_price),
                "currency": "USD"
            },
            "description": f"FeliMart Order #{order.id}"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        messages.error(request, 'Something went wrong creating the PayPal payment.')
        return redirect('order_confirm', order_id=order.id)

@login_required
def paypal_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        order.status = 'paid'
        order.save()
        request.session['cart'] = {}
        messages.success(request, f'Payment successful! Order #{order.id} is confirmed.')
    else:
        messages.error(request, 'Payment could not be completed.')

    return redirect('view_cart')

@login_required
def paypal_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.status = 'cancelled'
    order.save()
    messages.error(request, f'Payment cancelled for Order #{order.id}.')
    return redirect('view_cart')

@login_required
def shopping_advisor(request):
    response_text = None

    if request.method == 'POST':
        user_question = request.POST.get('question')
        products = Product.objects.all()

        product_list_text = "\n".join([
            f"- {p.name} ({p.category}, {p.rarity}): {p.description} Price: ${p.price}"
            for p in products
        ])

        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a helpful shopping assistant for FeliMart, a cat products store. 
Only recommend products from this exact list, do not invent products that aren't listed:

{product_list_text}

Customer question: {user_question}

Give a short, friendly recommendation in 1-2 sentences based only on the products above. 
Do not use em dashes (—) anywhere in your response, use commas or periods instead."""
                }
            ]
        )

        response_text = message.content[0].text

        AdvisorHistory.objects.create(
            user=request.user,
            question=user_question,
            answer=response_text
        )

    history = AdvisorHistory.objects.filter(user=request.user).order_by('-created_at')[:10]

    return render(request, 'store/advisor.html', {'response_text': response_text, 'history': history})