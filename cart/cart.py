from decimal import Decimal
from etrans.models import Product, ProductVariant
from django.conf import settings
from satchless.item import ItemLine, ItemList, partition


class Cart(object):

    def __init__(self, request):
       
       # Initialize the cart
      
        self.session = request.session #get current session 
        cart = self.session.get(settings.CART_SESSION_ID) #retrieve cart_session_key in the current session
        if not cart:
            # set cart_session_key to empty
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def create_line(self, variant, quantity, data):

        """Create a cart line for given variant, quantity and optional data.
        The `data` parameter may be used to differentiate between items with
        different customization options.
        """
        return self.lines.create(
            variant=variant, quantity=quantity, data=data or {})

    def add(self, variant, quantity=1, replace=False):

        #Adding a product to the cart or update its quantity
        #We expect our cart dictionary to use Ticket IDs as keys 
        #and a dictionary with quantity and price as value for each key
        
        ticket_id = str(variant.id)

        if ticket_id not in self.cart:
             self.cart[ticket_id]= {'quantity':0, 'price': str(variant.price)}

        if replace:
            self.cart[ticket_id]['quantity']= quantity
        else:
            self.cart[ticket_id]['quantity']+= quantity
        self.save()


    def save(self):
        #update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        #mark the session as modified to make sure it is saved
        self.session.modified = True


    def remove(self, ticket):
        #remove tickets from the cart

        ticket_id = str(ticket.id)
        if ticket_id in self.cart:
            del self.cart[ticket_id]
            self.save()

    def __iter__(self):

        #iterate over the items in the cart and get the ticket instance from the database
        ticket_ids = self.cart.keys()

        #get the ticket objects and add them to the cart item

        tickets = Product.objects.filter(id__in=ticket_ids)
        for ticket in tickets:
            self.cart[str(ticket.id)]['ticket']= ticket
        
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
     
       #Count all items in the cart      
        return sum(item['quantity'] for item in self.cart.values())


    def get_total_price(self):
        return sum(Decimal(item['price'])* item['quantity'] for item in self.cart.values()) 


    def clear(self):
        #remove cart from session
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True



    def all_lines(self):
        """
        Return a cached set of basket lines.

        This is important for offers as they alter the line models and you
        don't want to reload them from the DB as that information would be
        lost.
        """
        # if self.id is None:
        #     return self.lines.none()
        # if self._lines is None:
        #     self._lines = (
        #         self.lines
        #         .select_related('product', 'stockrecord')
        #         .prefetch_related(
        #             'attributes', 'product__images'))
        # return self._lines

    
     