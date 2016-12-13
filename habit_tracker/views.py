from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils import timezone

from .models import Habit, User


# def habits(request):
#     return HttpResponse("hello world from habit tracker")


def statistics(request):
    return HttpResponse("statistics page")


def about(request):
    return HttpResponse("about page")


def mainpage(request):
    habits_list = Habit.objects.order_by()
    context = {'habits_list': habits_list}
    return render(request, 'mainpage.html', context)


def resetdb(request):
    User.objects.all().delete()
    u1 = User(user_name = 'Niko', password = "pass")
    u2 = User(user_name='Kaisa', password="pass")
    u3 = User(user_name='Pavel', password="pass")
    u1.save()
    u2.save()
    u3.save()

    h1 = Habit(habit_name="run", repetitions_per_week=3, starting_date=timezone.now(), volume_with_units="10 min", user=u1)
    h2 = Habit(habit_name="eat", repetitions_per_week=7, starting_date=timezone.now(), volume_with_units="an apple", user=u2)
    h1.save()
    h2.save()
    no_users = len(User.objects.all())
    no_habits = len(Habit.objects.all())

    return HttpResponse("Database reseted with initial data.<br>" + str(no_users) + " users and " + str(no_habits) + " habits")
