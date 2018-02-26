from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from . import views

app_name = 'gogaga'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<pub_id>[0-9]+)/$', views.pub_details, name='pub_details'),
    url(r'^(?P<ticket_id>[0-9]+)/$', views.reserved, name='reserved'),
    url(r'^login/$', auth_views.login, {'template_name': 'gogaga/login.html'}, name='login'),
    url(r'^logout/$', auth_views.login, {'template_name': 'gogaga/logout.html'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^changepassword/$', views.changepassword, name='changepassword'),
    url(r'^password-reset/$', auth_views.password_reset, name='passwordreset'),
    url(r'^password-reset/done/$', auth_views.password_reset_done, name='passwordresetdone'),
    url(r'^password-reset/confirm/$', auth_views.password_reset_done, name='passwordresetdoneconfirm'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
