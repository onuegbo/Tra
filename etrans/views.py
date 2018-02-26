from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Company, Product, Collection
from django.contrib.auth.models import User
import datetime
import json
from django.conf import settings
from django.http import HttpResponsePermanentRedirect, JsonResponse
from django.template.response import TemplateResponse


from cart.utils import set_cart_cookie
from core.utils import serialize_decimal
from .filters import ProductCategoryFilter, ProductCollectionFilter

from .utils import (
    get_availability, get_product_attributes_data, get_product_images,
    get_variant_picker_data, handle_cart_form, product_json_ld,
    products_for_cart, get_product_list_context, products_with_details)


from rest_framework import generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from etrans.serializer import CompanySerializer
from etrans.serializer import UserSerializer
from etrans.permissions import IsOwnerOrReadOnly


from rest_framework import viewsets




#REST framework includes a number of permission classes that we can use to restrict who can access a given view


class CompanyViewSet(viewsets.ModelViewSet):

    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)  

    def perform_create(self, serializer):
        serializer.save(created =self.request.user)





class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer





















def category_list(request):
    c = Company.objects.order_by('name')
    companies=c.filter(is_hidden=False)
    return render(request, 'etrans/home.html', {'companies' : companies})



# def home(request, company_slug=None):
#     company = None
#     companies = Company.objects.all() #getting all companies
#     products = Product.objects.filter(is_featured=False) #getting all active tickets
#     if company_slug:
#             company = get_object_or_404(Company, slug=company_slug) #get company by slug
#             products = products.filter(company=company) #active tickets are filtered by company slug
#     return render(request, 'etrans/home.html', {'company': company, 'companies': companies, 'products': products})





def details(request, company_slug=None):
    company = None
    company = Company.objects.all()
    product = Product.objects.filter(is_featured =True) #getting all featured tickets
    if company_slug:
            company = get_object_or_404(Company, slug=company_slug) #get company by slug
            product = product.filter(company=company) #active tickets are filtered by company slug
    return render(request, 'etrans/list.html', {'products' : product, 'company': company})







def ticket_details(request, slug, product_id, form=None):

    """Product details page
    The following variables are available to the template:
    product:
        The Product instance itself.

    is_visible:
        Whether the product is visible to regular users (for cases when an
        admin is previewing a product before publishing).
        
    form:
        The add-to-cart form.

    price_range:
        The PriceRange for the product including all discounts.

    undiscounted_price_range:
        The PriceRange excluding all discounts.

    discount:
        Either a Price instance equal to the discount value or None if no
        discount was available.

    local_price_range:
        The same PriceRange from price_range represented in user's local
        currency. The value will be None if exchange rate is not available or
        the local currency is the same as site's default currency.
    """

    products = products_with_details(user=request.user)
    products = Product.objects.all()
    product = get_object_or_404(products, id=product_id)
    if product.get_slug() != slug:
        return HttpResponsePermanentRedirect(product.get_absolute_url())

    today = datetime.date.today()
    is_visible = (product.available_on is None or product.available_on <= today)

    if form is None:
        form = handle_cart_form(request, product, create_cart=False)[0]
    availability = get_availability(product, discounts=request.discounts, local_currency=request.currency)
    
    product_images = get_product_images(product)
   
    variant_picker_data = get_variant_picker_data(product, request.discounts, request.currency)

    product_attributes = get_product_attributes_data(product)

    # show_variant_picker determines if variant picker is used or select input
    show_variant_picker = all([v.attributes for v in product.variants.all()])

    json_ld_data = product_json_ld(product, product_attributes)
    
    return TemplateResponse(
        request, 'etrans/details.html',
        {'is_visible': is_visible,
         'form': form,
         'availability': availability,
         'product': product,
         'product_attributes': product_attributes,
         'product_images': product_images,
         'show_variant_picker': show_variant_picker,
         'variant_picker_data': json.dumps(variant_picker_data, default=serialize_decimal),
         'json_ld_product_data': json.dumps(json_ld_data, default=serialize_decimal)})

     
     #cart_product_form = CartAddProductForm()
     #return render(request,'etrans/details.html', {'ticket': ticket, 'cart_product_form': cart_product_form})    


def product_add_to_cart(request, slug, product_id):
    # types: (int, str, dict) -> None

    if not request.method == 'POST':
        return redirect(reverse( 'etrans:ticket_details',  kwargs={'product_id': product_id, 'slug': slug}))

    products = products_for_cart(user=request.user) #get user

    product = get_object_or_404(products, pk=product_id)

    form, cart = handle_cart_form(request, product, create_cart=True)

    if form.is_valid():
        form.save()
        if request.is_ajax():
            response = JsonResponse({'next': reverse('cart:index')}, status=200)
        else:
            response = redirect('cart:index')
    else:
        if request.is_ajax():
            response = JsonResponse({'error': form.errors}, status=400)
        else:
            response = ticket_details(request, slug, product_id, form)
    if not request.user.is_authenticated:
        set_cart_cookie(cart, response)
    return response





def all_list(request, company_slug=None):
    company = None
    companies = Company.objects.all() #getting all companies
    tickets = Product.objects.filter(is_featured=False) #getting all active tickets
    if company_slug:
            company = get_object_or_404(Company, slug=company_slug) #get company by slug
            tickets = tickets.filter(company=company) #active tickets are filtered by company slug
    return render(request, 'etrans/all.html', {'company': company, 'companies': companies, 'tickets': tickets})
   



# def collection_index(request, slug, pk):
#     collection = get_object_or_404(Collection, id=pk)
#     products = products_with_details(user=request.user).filter(
#         collections__id=collection.id).order_by('name')
#     product_filter = ProductCollectionFilter(
#         request.GET, queryset=products, collection=collection)
#     ctx = get_product_list_context(request, product_filter)
#     ctx.update({'object': collection})
#     return TemplateResponse(request, 'collection/index.html', ctx)


    
    





















   

   

