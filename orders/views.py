from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import get_connection, EmailMultiAlternatives
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


context = {}


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            context.update({'cart': cart, 'order': order})
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form})


def order_created():
    connection = get_connection()
    connection.open()

    html_content = render_to_string('orders/order/mail.html',
                                    context)
    text_content = render_to_string('orders/order/mail.txt', context)
    msg = EmailMultiAlternatives('Lenivastore - Заказ Оформлен',
                                 text_content, settings.EMAIL_HOST_USER,
                                 [context['order'].email], connection=connection)
    msg.attach_alternative(html_content, "text/html")
    mail_send = msg.send()

    connection.close()  # Cleanup
    return mail_send


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})
