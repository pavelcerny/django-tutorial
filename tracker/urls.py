from django.conf.urls import url

from . import views

app_name = 'tracker'

urlpatterns = [
    # ex: /tracker/
    url(r'^$', views.mainpage, name='mainpage'),
    # ex: /tracker/statistics
    url(r'^statistics$', views.statistics, name='statistics'),
    # ex: /tracker/about
    url(r'^about$', views.about, name='about'),
    url(r'^resetdb$', views.resetdb, name='resetdb'),

    # restart habit
    url(r'^habits/(?P<habit_id>[0-9]+)/restart/$', views.restart_habit, name='restart_habit'),
    # drop habit
    url(r'^habits/(?P<habit_id>[0-9]+)/drop/$', views.drop_habit, name='drop_habit'),
    # add habbit
    url(r'^habits$', views.add_habit, name='add_habit'),
    # edit habbit
    url(r'^habits/(?P<habit_id>[0-9]+)/edit$', views.edit_habit, name='edit_habit'),

    # show habit
    url(r'^habits/(?P<pk>[0-9]+)$', views.HabitView.as_view(), name='habit_details'),

]