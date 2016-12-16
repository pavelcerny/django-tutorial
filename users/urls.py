from django.conf.urls import url

from users import views

app_name = 'users'

urlpatterns = [
    # ex: /users/resetdb
    url(r'^resetdb$', views.resetdb, name='resetdb'),
    url(r'^login$', views.log_in, name='login'),
    url(r'^loged$', views.loged, name='loged'),


]