from django.conf import settings
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import pgettext_lazy
from satchless.item import InsufficientStock
from etrans.utils import allocate_stock, deallocate_stock
from . import GroupStatus







def cancel_order(order):
    """Cancels order by cancelling all associated shipment groups."""
    for group in order.groups.all():
        group.cancel()
        group.save()




def add_variant_to_delivery_group(group, variant, total_quantity, discounts=None, add_to_existing=True):

    """Adds total_quantity of variant to group.
    Raises InsufficientStock exception if quantity could not be fulfilled.

    By default, first adds variant  to existing lines with same variant.
    It can be disabled with setting add_to_existing to False.

    Order lines are created by increasing quantity of lines,
    as long as total_quantity of variant will be added.
    """
    quantity_left = (
        add_variant_to_existing_lines(group, variant, total_quantity)
        if add_to_existing else total_quantity
        )

    price = variant.get_price_per_item(discounts)
    while quantity_left > 0:
        stock = variant.select_stockrecord()
        if not stock:
            raise InsufficientStock(variant) #satchless
        quantity = (
            stock.quantity_available
            if quantity_left > stock.quantity_available
            else quantity_left
        )
        group.lines.create(
            product=variant.product,
            product_name=variant.display_product(),
            product_sku=variant.sku,
            quantity=quantity,
            unit_price_net=price,
            stock=stock
            )
        allocate_stock(stock, quantity)
        # refresh stock for accessing quantity_allocated
        stock.refresh_from_db()
        quantity_left -= quantity




def add_variant_to_existing_lines(group, variant, total_quantity):

    """Adds variant to existing lines with same variant.
    Variant is added by increasing quantity of lines with same variant,
    as long as total_quantity of variant will be added
    or there is no more lines with same variant .
    Returns quantity that could not be fulfilled with existing lines.
    """
    # order descending by lines' stock available quantity
    lines = group.lines.filter(product=variant.name, product_sku=variant.sku, stock__isnull=False).order_by(F('stock__quantity_allocated') - F('stock__quantity'))
    quantity_left = total_quantity
    for line in lines:
        quantity = (
            line.stock.quantity_available
            if quantity_left > line.stock.quantity_available
            else quantity_left)
        line.quantity += quantity
        line.save()
        allocate_stock(line.stock, quantity)
        quantity_left -= quantity
        if quantity_left == 0:
            break
    return quantity_left




