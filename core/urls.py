from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.home, name='core'),
    # url(r'^style-guide/', views.styleguide, name='styleguide'),
    # url(r'^impersonate/(?P<uid>\d+)/', views.impersonate,
    #     name='impersonate-start'),
    # url(r'^impersonate/stop/$', views.stop_impersonate,
    #     name='impersonate-stop'),
    url(r'^404', views.handle_404, name='handle-404'),
    # url(r'^manifest\.json$', views.manifest, name='manifest'),
   
]