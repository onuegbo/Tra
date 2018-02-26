import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.fields import HStoreField

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import F, Max, Q
from django.urls import reverse
from django.utils.encoding import smart_text
from django.utils.text import slugify
from django.utils.translation import pgettext_lazy
from django_prices.models import Price, PriceField
from prices import PriceRange
from satchless.item import InsufficientStock
from text_unidecode import unidecode
from versatileimagefield.fields import PPOIField, VersatileImageField

from discount.utils import calculate_discounted_price
from .utils import get_attributes_display_map
from django.contrib.auth.models import User

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight




#aka Category model
class Company(models.Model):
    #image = VersatileImageField(upload_to='company/%Y/%m/%d', ppoi_field='ppoi', blank=False)
    created = models.ForeignKey('auth.User', related_name='company', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=50)
    description = models.TextField(max_length=100, blank=True)
    numero_telephone = models.IntegerField(default = 0)
    slug = models.SlugField(max_length=50, unique=True) 
    is_hidden = models.BooleanField(default=False)

    
    
    class Meta:
        db_table= 'company'
        ordering = ['name']
        verbose_name = 'company'
        verbose_name_plural = 'Companies'
        permissions = (
            ('view_category',
             pgettext_lazy('Permission description', 'Can view categories')),
            ('edit_category',
             pgettext_lazy('Permission description', 'Can edit categories'))) 



    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('etrans:details', args=[self.slug])


   


    
   


class ProductType(models.Model):
    name = models.CharField(max_length=128)
    has_variants = models.BooleanField(default=True)
    product_attributes = models.ManyToManyField('ProductAttribute', related_name='products_types', blank=True)
    variant_attributes = models.ManyToManyField('ProductAttribute', related_name='product_variants_types', blank=True)
    is_shipping_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, name=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.name)




      

class ProductQuerySet(models.QuerySet):
    def available_products(self):
        today = datetime.date.today()
        return self.filter(
            Q(available_on__lte=today) | Q(available_on__isnull=True),
            Q(is_published=True))


class Product(models.Model):
    company= models.ForeignKey(Company, blank=False, related_name='products',  on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, related_name='products', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128)
    departure_time = models.DateTimeField()
    description = models.TextField()
    departure = models.CharField(max_length= 100)
    arrival = models.CharField(max_length= 100)
    price = PriceField(currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2) 
    available_on = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    attributes = HStoreField()
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_featured  = models.BooleanField(default=False)
   
    objects = ProductQuerySet.as_manager()

    class Meta:
        db_table='product'
        permissions = (
            ('view_product',
             pgettext_lazy('Permission description', 'Can view products')),
            ('edit_product',
             pgettext_lazy('Permission description', 'Can edit products')),
            ('view_properties',
             pgettext_lazy(
                 'Permission description', 'Can view product properties')),
            ('edit_properties',
             pgettext_lazy(
                 'Permission description', 'Can edit product properties')))

    def __iter__(self):
        if not hasattr(self, '__variants'):
            setattr(self, '__variants', self.variants.all())
        return iter(getattr(self, '__variants'))

    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, name=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.name)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('etrans:ticket_details', kwargs={'slug': self.get_slug(), 'product_id': self.id})
    

    def get_slug(self):
        return slugify(smart_text(unidecode(self.name)))

    def is_in_stock(self):
        return any(variant.is_in_stock() for variant in self)


    def is_available(self):
        today = datetime.date.today()
        return self.available_on is None or self.available_on <= today

    def get_first_image(self):
        first_image = self.images.first()
        return first_image.image if first_image else None


    def get_attribute(self, pk):
        return self.attributes.get(smart_text(pk))


    def set_attribute(self, pk, value_pk):
        self.attributes[smart_text(pk)] = smart_text(value_pk)

    def get_price_per_item(self, item, discounts=None):
        return item.get_price_per_item(discounts)

    def get_price_range(self, discounts=None):
        if self.variants.exists():
            prices = [
                self.get_price_per_item(variant, discounts=discounts)
                for variant in self]
            return PriceRange(min(prices), max(prices))
        price = calculate_discounted_price(self, self.price, discounts)
        return PriceRange(price, price)

    def get_gross_price_range(self, discounts=None):
        grosses = [
            self.get_price_per_item(variant, discounts=discounts)
            for variant in self]
        if not grosses:
            return None
        grosses = sorted(grosses, key=lambda x: x.tax)
        return PriceRange(min(grosses), max(grosses))

    
    

class ProductVariant(models.Model):
    sku = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=100, blank=True)
    BUS_TYPE = (
        ('C', 'Climatisee'),
        ('NC', 'Non climatisee'),  
    )
    bus_type = models.CharField(max_length = 2, choices =BUS_TYPE, blank=False, default='C', help_text='Bus climatisee' )
    price_override =PriceField(currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2, blank=True, null=True)
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    attributes = HStoreField()
    images = models.ManyToManyField('ProductImage', through='VariantImage')

    class Meta:
        app_label = 'etrans'
        db_table='productvariant'
        

    def __str__(self):
        return self.name or self.display_variant_attributes()

    def check_quantity(self, quantity):
        total_available_quantity = self.get_stock_quantity()
        if quantity > total_available_quantity:
            raise InsufficientStock(self) 

    def get_stock_quantity(self):
        return sum([stock.quantity_available for stock in self.stock.all()])

    
    def get_price_per_item(self, discounts=None):
        price = self.price_override or self.product.price
        price = calculate_discounted_price(self.product, price, discounts)
        return price


    def get_absolute_url(self):
        slug = self.product.get_slug()
        product_id = self.product.id
        return reverse('etrans:details', kwargs={'slug': slug, 'product_id': product_id})

    def as_data(self):
        return {
            'product_name': str(self),
            'product_id': self.product.pk,
            'variant_id': self.pk,
            'unit_price': str(self.get_price_per_item().gross)}

    def is_shipping_required(self):
        return self.product.product_type.is_shipping_required # model fields

    def is_in_stock(self):
        return any([stock.quantity_available > 0 for stock in self.stock.all()])


    def get_attribute(self, pk):
        return self.attributes.get(smart_text(pk))

    def set_attribute(self, pk, value_pk):
        self.attributes[smart_text(pk)] = smart_text(value_pk)

    def display_variant_attributes(self, attributes=None):
        if attributes is None:
            attributes = self.product.product_type.variant_attributes.all()
        values = get_attributes_display_map(self, attributes)
        if values:
            return ', '.join(
                ['%s: %s' % (smart_text(attributes.get(id=int(key))),
                             smart_text(value))
                 for (key, value) in values.items()])
        return ''


    def display_product(self):
        variant_display = str(self)
        product_display = (
            '%s (%s)' % (self.product, variant_display)
            if variant_display else str(self.product))
        return smart_text(product_display)

    def get_first_image(self):
        return self.product.get_first_image()


    def select_stockrecord(self, quantity=1):
        # By default selects stock with lowest cost price. If stock cost price
        # is None we assume price equal to zero to allow sorting.
        stock = [
            stock_item for stock_item in self.stock.all()
            if stock_item.quantity_available >= quantity]
        zero_price = Price(0, currency=settings.DEFAULT_CURRENCY)
        stock = sorted(
            stock, key=(lambda s: s.cost_price or zero_price), reverse=False)
        if stock:
            return stock[0]
    
    def get_cost_price(self):
        stock = self.select_stockrecord()
        if stock:
            return stock.cost_price 
        



   
class StockLocation(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (
            ('view_stock_location',
             pgettext_lazy('Permission description',
                           'Can view stock location')),
            ('edit_stock_location',
             pgettext_lazy('Permission description',
                           'Can edit stock location')))

    def __str__(self):
        return self.name
    


class Stock(models.Model):
    """There are five seats in Marcopolo X. 
        Three of them have already been sold to customers. 
        The stock records quantity is 5, quantity allocated is 3 and quantity available is 2.
    """
    # formula===> stock quantity = quantity allocated + quantity available
    
    variant = models.ForeignKey(ProductVariant, related_name='stock', on_delete=models.CASCADE)
    location = models.ForeignKey(StockLocation, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)], default=Decimal(1))
    quantity_allocated = models.IntegerField(validators=[MinValueValidator(0)], default=Decimal(0))
    cost_price = PriceField(currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2, blank=True, null=True)

    #Each stock records also has a cost price (the price that your store had to pay to obtain it).

    """Once a delivery group is marked as shipped, each stock record used to 
    fulfil its lines will have both its quantity at hand and 
    quantity allocated decreased by the number of items shipped
    """

    class Meta:
        db_table='stock'
        unique_together = ('variant', 'location')
       

    def __str__(self):
        return '%s - %s' % (self.variant.name, self.location)

    @property
    def quantity_available(self):
        return max(self.quantity - self.quantity_allocated, 0)




class ProductAttribute(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    

    class Meta:
        db_table='productattribute'
        ordering = ('slug', )
        

    def __str__(self):
        return self.name

    def get_formfield_name(self):
        return slugify('attribute-%s' % self.slug, allow_unicode=True)

    def has_values(self):
        return self.values.exists()


class AttributeChoiceValue(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    color = models.CharField(
        max_length=7, blank=True,
        validators=[RegexValidator('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')])
    attribute = models.ForeignKey(ProductAttribute, related_name='values', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'attribute')

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = VersatileImageField(upload_to='products', ppoi_field='ppoi', blank=False)
    ppoi = PPOIField()
    alt = models.CharField(max_length=128, blank=True)
    order = models.PositiveIntegerField(editable=False)

    class Meta:
        ordering = ('order', )
        app_label = 'etrans'

    def get_ordering_queryset(self):
        return self.product.images.all()

    def save(self, *args, **kwargs):
        if self.order is None:
            qs = self.get_ordering_queryset()
            existing_max = qs.aggregate(Max('order'))
            existing_max = existing_max.get('order__max')
            self.order = 0 if existing_max is None else existing_max + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        qs = self.get_ordering_queryset()
        qs.filter(order__gt=self.order).update(order=F('order') - 1)
        super().delete(*args, **kwargs)


class VariantImage(models.Model):
    variant = models.ForeignKey('ProductVariant', related_name='variant_images', on_delete=models.CASCADE)
    image = models.ForeignKey(ProductImage, related_name='variant_images', on_delete=models.CASCADE)



class Collection(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField()
    products = models.ManyToManyField(Product, blank=True, related_name='collections')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
          return reverse('etrans:collection',   kwargs={'pk': self.id, 'slug': self.slug})







































GENDER_CHOICES = (
('M', 'Male'),
('F', 'Female'),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES, default='M')
    bio = models.TextField(max_length=1024, null=True, blank=True)


















# class Ticket(models.Model):

#     TICKET_TYPE = (
#         ('I', 'Individuelle'),
#         ('F', 'Famille'),  
#     )
#     genre = models.CharField(max_length = 1, choices =TICKET_TYPE, blank=False, default='I', help_text='genre de ticket' ) 
    
#     updated_by = models.ForeignKey(User, null=True, related_name='+', editable=False)
#     bought_by= models.ForeignKey(User, null=True, related_name='tickets', editable=False)
#     travelprogram = models.ForeignKey('TravelProgram', editable=False, related_name='tickets', null= True, on_delete=models.CASCADE)
#     company = models.ForeignKey('Company', related_name='companyticket', null = True, on_delete=models.CASCADE)
#     bought_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
#     telephone = models.PositiveIntegerField()
#     booking_seats_num =models.IntegerField()
   
    

#     def __str__(self):
#         return self.bought_by
    
     
#     class Meta:
#         ordering = ['bought_by']

#     @property
#     def total(self):
#         total = self.fare*self.booking_seats_num
#         return total



# TravelProgram and Clients are OneToMany Relationship
#TravelProgram are sold to Clients
#Each Traveller is entitiled to one Ticket at a time

# There must be a OneToManyRelationship between the Company and the TciketProgram,
# so as to map a company to a published travel program