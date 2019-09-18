from django.shortcuts import render
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import get_connection, EmailMultiAlternatives

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


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
            context = {'cart': cart, 'order': order}
            connection = get_connection()
            connection.open()

            html_content = render_to_string('orders/order/mail.html',
                                            context)
            text_content = render_to_string('orders/order/mail.txt', context)
            msg = EmailMultiAlternatives('Lenivastore - Заказ Оформлен',
                                         text_content, settings.EMAIL_HOST_USER,
                                         [order.email], connection=connection)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            connection.close()  # Cleanup
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form})
