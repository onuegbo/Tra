from django.db import models
from etrans.models import Product, ProductVariant, Stock
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from django.utils.translation import pgettext_lazy
from django_fsm import FSMField, transition
from satchless.item import ItemLine, ItemSet
from .transition import (cancel_delivery_group, process_delivery_group, ship_delivery_group)
from . import GroupStatus, OrderStatus
from django_prices.models import PriceField
from prices import FixedDiscount, Price
from django.db.models import F, Max, Q
    



class OrderQuerySet(models.QuerySet):
    """Filters orders by status deduced from shipment groups."""

    def open(self):
        """Orders having at least one shipment group with status NEW."""
        return self.filter(Q(groups__status=GroupStatus.NEW))

    def closed(self):
        """Orders having no shipment groups with status NEW."""
        return self.filter(~Q(groups__status=GroupStatus.NEW))

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        db_table='order'
        ordering = ('-created',)

    def __str__(self):
        return '#%d' % (self.id,)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def __iter__(self):
        return iter(self.groups.all())

    def __repr__(self):
        return '<Order #%r>' % (self.id,)

    def is_shipping_required(self):
        return any(group.is_shipping_required() for group in self.groups.all())

    def get_lines(self):
        return OrderLine.objects.filter(delivery_group__order=self)

    @property
    def status(self):
        """Order status deduced from shipment groups."""
        statuses = set([group.status for group in self.groups.all()]) #groups (related_name=DeliveryGroup)
        return (
                OrderStatus.OPEN if GroupStatus.NEW in statuses
                else OrderStatus.CLOSED
                 )
    @property
    def is_open(self):
        return self.status == OrderStatus.OPEN
    
    def get_status_display(self):
        """Order status display text."""
        return dict(OrderStatus)[self.status]

    def can_cancel(self):
        return self.status == OrderStatus.OPEN

   
class DeliveryGroup(models.Model, ItemSet):
    """Represents a single tickets.
    A single order can consist of tickets groups.
    """
    order = models.ForeignKey(Order, related_name='groups', editable=False, on_delete=models.CASCADE)
    status = FSMField(max_length=30, default='GroupStatus.NEW', choices=GroupStatus.CHOICES, protected=True)
    shipping_method_name = models.CharField(max_length=255, null=True, default=None, blank=True, editable=False)
    tracking_number = models.CharField(max_length=255, default='', blank=True)
    last_updated = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return pgettext_lazy(
            'Shipment group str', 'Shipment #%s') % self.pk

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __iter__(self):
        if self.id:
            return iter(self.lines.all())
        return super().__iter__()

    @transition(field=status, source=GroupStatus.NEW, target=GroupStatus.NEW)
    def process(self, cart_lines, discounts=None):
        process_delivery_group(self, cart_lines, discounts)

    @transition(field=status, source=GroupStatus.NEW, target=GroupStatus.SHIPPED)
    def ship(self, tracking_number=''):
        ship_delivery_group(self, tracking_number)

    @transition( field=status, source=[GroupStatus.NEW, GroupStatus.SHIPPED], target=GroupStatus.CANCELLED)
    def cancel(self):
        cancel_delivery_group(self)


    @property
    def shipping_required(self):
        return self.shipping_method_name is not None

    def get_total_quantity(self):
        return sum([line.get_quantity() for line in self])

    def is_shipping_required(self):
        return self.shipping_required

    def can_ship(self):
        return self.is_shipping_required() and self.status == GroupStatus.NEW

    def can_cancel(self):
        return self.status != GroupStatus.CANCELLED

    def can_edit_lines(self):
        return self.status not in {GroupStatus.CANCELLED, GroupStatus.SHIPPED}



class OrderLine(models.Model, ItemLine):
    #order = models.ForeignKey(Order, related_name='items', null=True)
    delivery_group = models.ForeignKey( DeliveryGroup, related_name='lines', editable=False, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='+', null=True)
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=128, null=True)
    product_sku = models.CharField(max_length=32, null=True)
    unit_price_net = models.DecimalField(max_digits=12, decimal_places=4)
    unit_price_gross = models.DecimalField(max_digits=12, decimal_places=4)
    quantity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)])
 
    class Meta:
        db_table='orderline'
        
    
    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self, **kwargs):
        return self.price * self.quantity


class OrderHistoryEntry(models.Model):
    date = models.DateTimeField(default=now, editable=False)
    order = models.ForeignKey(Order, related_name='history', on_delete=models.CASCADE)  
    status = models.CharField(max_length=32, choices=OrderStatus.CHOICES)
    comment = models.CharField(max_length=100, default='', blank=True)
    

    class Meta:
        db_table='orderhistory'
        ordering = ('date',)
    
    def __str__(self):
        return pgettext_lazy(
            'Order history entry str',
            'OrderHistoryEntry for Order #%d') % self.order.pk

