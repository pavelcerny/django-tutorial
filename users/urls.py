from django.conf.urls import url

from users import views

app_name = 'users'

urlpatterns = [
    # ex: /users/resetdb
    url(r'^resetdb$', views.resetdb, name='resetdb')

]