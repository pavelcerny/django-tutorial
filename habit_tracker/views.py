from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Habit


# def habits(request):
#     return HttpResponse("hello world from habit tracker")


def statistics(request):
    return HttpResponse("statistics page")


def about(request):
    return HttpResponse("about page")


class HabitsView(generic.ListView):
    template_name = 'habits.html'
    context_object_name = 'habits_list'

    def get_queryset(self):
        """
        Return list of all habits
        """
        return Habit.objects.order_by()

