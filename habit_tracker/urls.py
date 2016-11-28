from django.conf.urls import url

from . import views

app_name = 'habit_tracker'

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.habits, name='habits'),
    url(r'^statistics$', views.statistics, name='statistics'),
    url(r'^about$', views.about, name='about'),
]