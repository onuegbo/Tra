from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .import views

app_name = 'cart'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^update/(?P<variant_id>\d+)/$', views.update, name='update-line'),
    url(r'^summary/$', views.summary, name='cart-summary'),
    url(r'^shipingoptions/$', views.get_shipping_options, name='shipping-options')
]