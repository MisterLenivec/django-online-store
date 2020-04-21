from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.template.loader import render_to_string
from django.core.mail import get_connection, EmailMultiAlternatives
import weasyprint
from io import BytesIO

from orders.models import Order


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % Decimal(order.get_total_cost()).quantize(Decimal('.01')),
        'item_name': 'Заказ {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'RUB',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled'))
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'order': order, 'form': form})


@csrf_exempt
def payment_done(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()

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
                            settings.STATIC_ROOT + 'css/style.css')])
    msg = EmailMultiAlternatives(subject, message,
                                 settings.EMAIL_HOST_USER, [order.email],
                                 connection=connection)
    msg.attach_alternative(html_content, "text/html")
    msg.attach('order_{}.pdf'.format(order.id), out.getvalue(),
                 'application/pdf')
    msg.send()

    connection.close()  # Cleanup
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
