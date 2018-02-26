from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from .import views
from account import views as accounts_views
from django.contrib.auth import views as auth_views




from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'company', views.CompanyViewSet)
router.register(r'users', views.UserViewSet)





app_name = 'etrans'
urlpatterns =[

    url(r'^', include(router.urls)),
 
    








    url(r'^$', views.category_list, name='home'),
    #url(r'^(?P<company_slug>[-\w]+)/$', views.home, name='product_list_by_category'),

    
    url(r'^companys/(?P<company_slug>[-\w]+)/$', views.details, name='details'),
    url(r'^alltickets/$', views.all_list, name='all_list'),
    url(r'^(?P<slug>[a-z0-9-_]+?)-(?P<product_id>[0-9]+)/$', views.ticket_details, name='ticket_details'),
    url(r'(?P<slug>[a-z0-9-_]+?)-(?P<product_id>[0-9]+)/add/$', views.product_add_to_cart, name="add-to-cart"),

    # url(r'^collection/(?P<slug>[a-z0-9-_/]+?)-(?P<pk>[0-9]+)/$', views.collection_index, name='collection'),



   


    
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='etrans/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='etrans/password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),

    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='etrans/password_reset_done.html'),
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='etrans/password_reset_confirm.html'),
        name='password_reset_confirm'),

    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='etrans/password_reset_complete.html'),
        name='password_reset_complete'),


    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='etrans/password_change.html'),
    name='password_change'),

    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='etrans/password_change_done.html'),
    name='password_change_done'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 



# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
# Remember that we only serve static files this way during the development. In a
# production environment, you should never serve static files with Django.