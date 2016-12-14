from django.conf.urls import url

from . import views

app_name = 'habit_tracker'

urlpatterns = [
    # ex: /habit_tracker/
    url(r'^$', views.mainpage, name='mainpage'),
    # ex: /habit_tracker/statistics
    url(r'^statistics$', views.statistics, name='statistics'),
    # ex: /habit_tracker/about
    url(r'^about$', views.about, name='about'),
    url(r'^resetdb$', views.resetdb, name='resetdb'),

    # restart habit
    url(r'^habits/(?P<habit_id>[0-9]+)/restart/$', views.restart_habit, name='restart_habit'),
    # drop habit
    url(r'^habits/(?P<habit_id>[0-9]+)/drop/$', views.drop_habit, name='drop_habit'),
]