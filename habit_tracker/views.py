from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils import timezone

from .models import Habit, User, Occurrence

SUCCESS = "success"
FAIL = "fail"
NO_RECORD = "no-record"
DAYS_DISPLAYED = 7

def date_lt(first, second):
    if first.year < second.year:
        return True
    else:
        if first.year > second.year:
            return False
    if first.month < second.month:
        return True
    else:
        if first.month > second.month:
            return False
    if first.day < second.day:
        return True
    else:
        if first.day > second.day:
            return False

    return False


def helloworld(request):
   return HttpResponse("hello world from habit tracker")


def statistics(request):
    return HttpResponse("statistics page")


def about(request):
    return HttpResponse("about page")


def get_records_table(for_habit, n):
    """
    Returns table with SUCCESS/FAIL/NO-RECORD fields for last n days of given habit
    :param for_habit: habit to be analysed
    :param n: number of last days we are interested in
    :return: table with SUCCESS/FAIL/NO-RECORD fields
    """
    today = timezone.now().date()
    n_days_ago = today - timezone.timedelta(days=n)

    # find successes in last n days
    successes = Occurrence.objects.filter(
        habit=for_habit,
        date__date__gt=n_days_ago,
        date__date__lte=today
        ).order_by('-date')
    # get dates of successes
    successful_days = [s.date.date() for s in successes]

    # init new table with FAILs for last n days
    table = [FAIL] * n;

    # fill SUCCESSes in the table
    i = n-1
    # iterating last n dates
    for day in ((timezone.now() - timezone.timedelta(days=x)).date() for x in range(0, n)):
        if day in successful_days:
            table[i] = SUCCESS;
        else:
            start = for_habit.starting_date.date()
            if date_lt(day,start):
                table[i] = NO_RECORD
        i-=1

    return table


def get_speed(record_table):
    """
    Return ratio success:total for given record table
    :param record_table: array with SUCCESS/FAIL/NO-RECORD fields
    :return: ration - number of suceess divided by number of tries
    """
    successes = 0
    total = 0
    for entry in record_table:
        if entry == SUCCESS:
            successes+=1
        if entry != NO_RECORD:
            total+=1
    return successes/total


def get_dates(days_dispayed):

    return [timezone.now().date()] * days_dispayed


def mainpage(request):
    # get all habits
    habits_list = Habit.objects.order_by('order')

    # create HabitItems
    habit_items = []
    for habit in habits_list:
        records = get_records_table(habit,DAYS_DISPLAYED)
        computed_speed = get_speed(records)
        hi = HabitItem(
            records_table = records,
            habit= habit,
            speed = computed_speed)
        habit_items.append(hi)

    # create Days to be displayed
    dates = get_dates(DAYS_DISPLAYED)
    # pass the objects
    context = {'habit_items': habit_items,
               'dates': dates}
    return render(request, 'mainpage.html', context)


class HabitItem:
    records_table = []
    habit = None
    speed = 0

    def __init__(self, records_table, habit, speed):
        self.records_table = records_table
        self.habit = habit
        self.speed = speed

def resetdb(request):
    User.objects.all().delete()
    u1 = User(user_name = 'Niko', password = "pass")
    u2 = User(user_name='Kaisa', password="pass")
    u3 = User(user_name='Pavel', password="pass")
    u1.save()
    u2.save()
    u3.save()

    h1 = Habit(habit_name="run", repetitions_per_week=3, starting_date=timezone.now()-timezone.timedelta(days=20), volume_with_units="10 min", user=u1, order=1)
    h2 = Habit(habit_name="eat", repetitions_per_week=7, starting_date=timezone.now()-timezone.timedelta(days=3), volume_with_units="an apple", user=u2, order=2)
    h3 = Habit(habit_name="code", repetitions_per_week=7, starting_date=timezone.now()-timezone.timedelta(days=3), volume_with_units="1h", user=u2, order=1)
    h1.save()
    h2.save()
    h3.save()
    no_users = len(User.objects.all())
    no_habits = len(Habit.objects.all())

    o1 = Occurrence(habit=h1, date=timezone.now())
    o2 = Occurrence(habit=h1, date=timezone.now()- timezone.timedelta(days=5))
    o3 = Occurrence(habit=h1, date=timezone.now()- timezone.timedelta(days=6))
    o4 = Occurrence(habit=h1, date=timezone.now()- timezone.timedelta(days=8))
    o1.save()
    o2.save()
    o3.save()
    o4.save()

    return HttpResponse("Database reseted with initial data.<br>" + str(no_users) + " users and " + str(no_habits) + " habits")
