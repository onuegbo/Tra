from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import OrderLine, Product, ProductVariant, DeliveryGroup
from .forms import OrderCreateForm
from cart.cart import Cart  #from  cart app .cart.py  import Cart class
from .tasks import order_created
from .utils import add_variant_to_delivery_group, add_variant_to_existing_lines



def order_create(request):
        cart = Cart(request) #calling the Cart class object
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                    order = form.save()
                    for item in cart:
                        #group = DeliveryGroup.objects.create(order=order, status='GroupStatus.NEW', tracking_number='0012ERXX')
                        OrderLine.objects.create(order=order, product=item['ticket'], price=item['price'], quantity=item['quantity'])
                        #add_variant_to_delivery_group(group=group, variant=item['ticket'], total_quantity=item['quantity'], discounts=None, add_to_existing=False)
                   
                    # clear the cart
                    cart.clear()
                    # launch asynchronous task
                    order_created.delay(order.id)
                    request.session['order_id'] = order.id # redirect to the payment

            return redirect(reverse('payment:process'))

        else:

                form = OrderCreateForm()
                return render(request,'orders/create.html', {'cart': cart, 'form': form})