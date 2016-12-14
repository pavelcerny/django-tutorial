from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect

from .forms import AddHabitForm
from .models import Habit, User, Record

SUCCESS = "success"
FAIL = "fail"
NO_RECORD = "no-record"
DAYS_DISPLAYED = 7
FUTURE_DAYS_DISPLAYED = 4
DEFAULT_USER = "Niko"

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
    successes = Record.objects.filter(
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
    iterator = reversed(range(0, days_dispayed))
    # lambda function, get day.date()
    dates = ((timezone.now() - timezone.timedelta(days=x)).date() for x in iterator)
    return dates


def get_future_dates(days_displayed):
    iterator = range(1, days_displayed+1)
    # lambda function, get day.date()
    dates = ((timezone.now() + timezone.timedelta(days=x)).date() for x in iterator)
    return dates


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
    future_dates = get_future_dates(FUTURE_DAYS_DISPLAYED)
    # pass the objects
    context = {'habit_items': habit_items,
               'dates': dates,
               'future_dates':future_dates}
    return render(request, 'tracker/mainpage.html', context)


class HabitItem:
    records_table = []
    habit = None
    speed = 0

    def __init__(self, records_table, habit, speed):
        self.records_table = records_table
        self.habit = habit
        self.speed = speed


class HabitView(generic.DetailView):
    model = Habit
    template_name = 'tracker/habitdetail.html'


def restart_habit(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id)

    try:
        habit_records = habit.record_set.all().delete()
    except (KeyError, Habit.DoesNotExist):
        return HttpResponse ("can't restart habit does not exist " + str(habit_id))
    else:
        # reset day started
        habit.starting_date = timezone.now();
        habit.save()
        message = "restarted habit "+str(habit_id)
        context = {'message': message}
        return render(request, 'tracker/restart_habit.html', context)


def drop_habit(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id)

    try:
        habit.delete()
    except (KeyError, Habit.DoesNotExist):
        return HttpResponse("can't drop, habit does not exist " + str(habit_id))
    else:
        message = "droped habit " + str(habit_id)
        context = {'message': message}
        return render(request, 'tracker/drop_habit.html', context)


def find_user():
    # TODO validate user exist, what if don't exist
    user = User.objects.get(user_name=DEFAULT_USER)

    return user


def add_habit(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddHabitForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = find_user()

            # process the data in form.cleaned_data as required
            f = form.cleaned_data
            h = Habit()
            h.habit_name = f['habit_name']
            h.repetitions_per_week = f['repetitions_per_week']
            h.volume_with_units = f['volume_with_units']
            h.starting_date = f['starting_date']
            # TODO order is last+1 habit of user
            h.order = f['order']

            h.user = user

            h.save()

            # redirect to a new URL:
            # i.e. return HttpResponseRedirect('/thanks/')
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddHabitForm()

    return render(request, 'tracker/add_habit.html', {'form': form})


def resetdb(request):
    User.objects.all().delete()
    u1 = User(user_name = DEFAULT_USER, password = "pass")
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

    r1 = Record(habit=h1, date=timezone.now())
    r2 = Record(habit=h1, date=timezone.now() - timezone.timedelta(days=5))
    r3 = Record(habit=h1, date=timezone.now() - timezone.timedelta(days=6))
    r4 = Record(habit=h1, date=timezone.now() - timezone.timedelta(days=8))
    r1.save()
    r2.save()
    r3.save()
    r4.save()

    message = "Database reseted with initial data. New " + str(no_users) + " users and new " + str(no_habits) + " habits"
    context = {'message': message}
    return render(request, 'tracker/resetdb.html', context)
