from django.shortcuts import render

import json

from django.template.response import TemplateResponse
from django.contrib import messages
from django.utils.translation import pgettext_lazy
#from impersonate.views import impersonate as orig_impersonate, stop_impersonate

#from ..dashboard.views import staff_member_required
from etrans.utils import products_with_availability, products_for_homepage
# from ..userprofile.models import User
from .utils.schema import get_webpage_schema


def home(request):
    products = products_for_homepage()[:8]
    products = products_with_availability(
        products, discounts=request.discounts, local_currency=request.currency)
    # webpage_schema = get_webpage_schema(request)
    return TemplateResponse(
        request, 'core/home.html', {
            'parent': None,
            'products': products})

            #  return render(request, 'etrans/home.html', {'companys' : companys})


# @staff_member_required
# def styleguide(request):
#     return TemplateResponse(request, 'styleguide.html')


# def impersonate(request, uid):
#     response = orig_impersonate(request, uid)
#     if request.session.modified:
#         msg = pgettext_lazy(
#             'Impersonation message',
#             'You are now logged as {}'.format(User.objects.get(pk=uid)))
#         messages.success(request, msg)
#     return response


def handle_404(request, exception=None):
    return TemplateResponse(request, '404.html', status=404)


# def manifest(request):
#     site = request.site
#     ctx = {
#         'description': site.settings.description,
#         'name': site.name,
#         'short_name': site.name}
#     return TemplateResponse(
#         request, 'manifest.json', ctx, content_type='application/json')