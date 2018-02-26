"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from mysite import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.schemas import get_schema_view
schema_view = get_schema_view(title='Pastebin API')


urlpatterns = [
    url(r'^$', views.login_redirect, name='login_redirect'),
    #url(r'^gogaga/', include('gogaga.urls')),
    
  
  
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^schema/$', schema_view),
    
    url(r'^cart/', include ('cart.urls')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^account/', include ('account.urls')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^payment/', include('payment.urls', namespace='payment')),
    url(r'^etrans/', include('etrans.urls', namespace='etrans')),
    url('', include('pwa.urls')),
    # url(r'^shipping/', include('shipping.urls')),
    # url(r'^discount/', include('discount.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^admin/', admin.site.urls),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


