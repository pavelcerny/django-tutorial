from django.conf.urls import url

from . import views

app_name = 'habit_tracker'

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
]