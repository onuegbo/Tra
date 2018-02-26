# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Order
from django.core.mail import send_mail


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\Your order id is {}.'.format(order.first_name,order.id)
    mail_sent = send_mail(subject,
                          message,
                          'admin@mysite.com',
                          [oliveramaobi2017@gmail.com]
                          )
    return mail_sent