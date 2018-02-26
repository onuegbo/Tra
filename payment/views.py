from django.core.urlresolvers import reverse
from django.shortcuts import render
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt


def payment_process(request):
    order_id = request.session.get('order_id') #session from the Order app
    order = get_object_or_404(Order, id=order_id) #passing the session order_id back as id
    host = request.get_host()
    # What you want the button to do.
    paypal_dict = {
        "business":  settings.PAYPAL_RECEIVER_EMAIL,
        "amount": '%.2f' % order.get_total_cost().quantize(Decimal('.01')),
        "item_name":  'Order {}'.format(order.id),
        "invoice":   str(order.id), #passing order.id to paypal
        'currency_code': 'USD',
        "notify_url":  'http://{}{}'.format(host, reverse('paypal-ipn')),
        "return_url":  'http://{}{}'.format(host, reverse('payment:successful')),
        "cancel_return":  'http://{}{}'.format(host, reverse('payment:canceled')),   
    }

  # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'order': order, 'form':form})



@csrf_exempt
def successful(request):
 return render(request, 'payment/successful.html')

@csrf_exempt
def canceled(request):
 return render(request, 'payment/canceled.html')
