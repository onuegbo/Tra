from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from django.dispatch import receiver
from orders.models import Order, OrderLine
from etrans.models import Company, Product
#from django.db.models.signals import post_save
from django.db.models import F
import django.dispatch
from etrans.utils import (allocate_stock, decrease_stock)

#payment notification receiver

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs): 
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # payment was successful
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        # mark the order as paid
        order.paid = True
        order.save()




# @receiver(post_save, sender=Order, weak=False, dispatch_uid='decrement')
# def decrement(sender, instance, created, **kwargs):

#     TravelProgram.objects.select_related().filter(pk=10).update(number_of_seats=F('number_of_seats') - orderitems.quantity)

















# Field lookups are how you specify the meat of an SQL WHERE clause. 
# They’re specified as keyword arguments to the QuerySet methods filter(), exclude() and get().



#post_save.connect(payment_notification, sender=Order, weak=False, dispatch_uid='havepaid')

    #........... Look up that span relationship.............

    # >>> Entry.objects.filter(blog__name='Beatles Blog') forward
    # >>> Blog.objects.filter(entry__headline__contains='Lennon') backward

   # some_entry.id == other_entry.id
    # Entry.objects.all().update(n_pingbacks=F('n_pingbacks') + 1)

    # Change every TravelProgram number_of seats.
    # TravelProgram.objects.all().update(number_of_seats=F('number_of_seats') - b.quantity)  
    # 
    #    
  #..........related manager..............
    #  b = Blog.objects.get(id=1)
    #  >>> b.entries.all() # Returns all Entry objects related to Blog.

    # b.entries is a Manager that returns QuerySets.
        # >>> b.entries.filter(headline__contains='Lennon')
        # >>> b.entries.count()