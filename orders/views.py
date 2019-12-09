from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import get_connection, EmailMultiAlternatives
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt

import weasyprint

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.cupon:
                order.cupon = cart.cupon
                order.discount = cart.cupon.discount
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            request.session['order_id'] = order.id
            if order.card_paid:
                return redirect(reverse('payment:process'))
            else:
                return offline_paid(request, cart)
    else:
        if request.user.is_authenticated:
            form = OrderCreateForm(instance=request.user)
        else:
            form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form})


@csrf_exempt
def offline_paid(request, cart):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    connection = get_connection()
    connection.open()

    subject = 'Lenivastore - Заказ номер {} оформлен'.format(order.id)
    message = render_to_string('orders/order/mail.txt',
                               {'order': order})
    html_content = render_to_string('orders/order/mail.html',
                                    {'order': order})
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out,
                            stylesheets=[weasyprint.CSS(
                            settings.STATIC_ROOT + '/css/style.css')])  # + 'css/bootstrap.min.css'
    msg = EmailMultiAlternatives(subject, message,
                                 settings.EMAIL_HOST_USER, [order.email],
                                 connection=connection)
    msg.attach_alternative(html_content, "text/html")
    msg.attach('order_{}.pdf'.format(order.id), out.getvalue(),
                 'application/pdf')
    msg.send()

    connection.close()  # Cleanup
    return render(request, 'orders/order/offline_paid_order_done.html',
                  {'order': order, 'cart': cart})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_PDF(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
               stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/style.css')])  # + 'css/bootstrap.min.css'
    return response
