from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from users import views

app_name = 'users'

urlpatterns = [
    # resetingdb works from tracker app
    # url(r'^resetdb$', views.resetdb, name='resetdb'),

    # login & logout
    url(r'^login/$', auth_views.login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout$', views.log_out, name='logout'),

    # loged in & loged out
    url(r'^loged$', views.loged, name='loged'),
    url(r'^logedout$', views.logedout, name='logedout'),
    url(r'^', include('registration.backends.simple.urls')),

]
