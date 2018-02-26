from django.conf.urls import url
from . import views


urlpatterns = [
 url(r'^process/$', views.payment_process, name='process'),
 url(r'^successful/$', views.successful, name='successful'),
 url(r'^canceled/$', views.canceled, name='canceled'),
]