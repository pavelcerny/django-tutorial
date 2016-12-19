from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .forms import AddHabitForm
from .models import Habit, Record
from django.contrib.auth.models import User

class RecordValues:
    SUCCESS, FAIL, NO_RECORD = range(3)

DAYS_DISPLAYED = 7
FUTURE_DAYS_DISPLAYED = 4
DEFAULT_USER = "niko"


def now():
    return timezone.now().astimezone().date()


def date_lt(first, second):
    '''
    return True for first date < second date
    :param first:
    :param second:
    :return:
    '''
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
    today = now()
    tomorrow = today + timezone.timedelta(days=1)
    n_days_ago = today - timezone.timedelta(days=n)

    # find successes in last n days
    successes = Record.objects.filter(
        habit=for_habit,
        date__gt=n_days_ago,
        date__lt=tomorrow
        ).order_by('-date')
    # get dates of successes
    successful_days = [s.date for s in successes]

    # init new table with FAILs for last n days
    table = [RecordValues.FAIL] * n;

    # fill SUCCESSes in the table
    i = n-1
    # iterating last n dates
    start = for_habit.starting_date
    for day in (now() - timezone.timedelta(days=x) for x in range(0, n)):
        if day in successful_days:
            table[i] = RecordValues.SUCCESS;
        else:
            if date_lt(day,start):
                table[i] = RecordValues.NO_RECORD
        i-=1

    return table


def get_speed(record_table):
    """
    Go through given record table and return ratio success:total
    :param record_table: array with SUCCESS/FAIL/NO-RECORD fields
    :return: ration - number of suceess divided by number of tries
    """
    successes = 0
    total = 0
    for entry in record_table:
        if entry == RecordValues.SUCCESS:
            successes += 1
        if entry != RecordValues.NO_RECORD:
            total += 1
    return successes/total


def get_dates(days_displayed):
    iterator = reversed(range(0, days_displayed))
    # lambda function, get dates i.e. [(2016,12,3), (2016,12,4), (2016,12,5), ... , today.date()]
    dates = (now() - timezone.timedelta(days=x) for x in iterator)
    return dates


def get_future_dates(days_displayed):
    iterator = range(1, days_displayed+1)
    # lambda function, get dates i.e. [today.date()+1, ..., (2016,12,17), (2016,12,18), (2016,12,21)]
    dates = (now() + timezone.timedelta(days=x) for x in iterator)
    return dates


@login_required
def mainpage_controller(request):
    user = request.user

    # get all habits
    habits_list = Habit.objects.filter(user=user).order_by('order')

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
               'future_dates':future_dates,
               'record_values': RecordValues,
               'username': user.username}
    return render(request, 'tracker/mainpage.html', context)


def mainpage_with_styles(request):
    user = request.user

    # get all habits
    habits_list = Habit.objects.filter(user=user).order_by('order')

    # create HabitItems
    habit_items = []
    for habit in habits_list:
        records = get_records_table(habit, DAYS_DISPLAYED)
        computed_speed = get_speed(records)
        hi = HabitItem(
            records_table=records,
            habit=habit,
            speed=computed_speed)
        habit_items.append(hi)

    # create Days to be displayed
    dates = get_dates(DAYS_DISPLAYED)
    future_dates = get_future_dates(FUTURE_DAYS_DISPLAYED)
    # pass the objects
    context = {'habit_items': habit_items,
               'dates': dates,
               'future_dates': future_dates,
               'record_values': RecordValues,
               'username': user.username}
    # return render(request, 'tracker/mainpage_controller.html', context)
    return render(request, 'index_server.html', context)


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


def is_author(request, habit):
    if habit.user == request.user:
        return True
    else:
        return False


def can_modify_habit(request, habit_id):
    # find habit or raise 404 error
    habit = get_object_or_404(Habit, pk=habit_id)
    try:
        if habit.user == request.user:
            return True, habit
        else:
            return False, habit
    except(KeyError, Habit.DoesNotExist):
        return False, None


@login_required
def restart_habit_controller(request, habit_id):
    # only author can restart
    can_restart, habit = can_modify_habit(request, habit_id)

    if not can_restart:
        # report error
        return HttpResponse("you can't restart this habit")
    else:
        # restart
        restart_habit(habit)
        message = "restarted habit " + str(habit_id)
        context = {'message': message}
        return render(request, 'tracker/restart_habit.html', context)


def restart_habit(habit):
    # delete all habit's records
    habit.record_set.all().delete()

    # set starting_date to today
    habit.starting_date = now();
    habit.save()


@login_required
def drop_habit_controller(request, habit_id):
    # only author can drop
    can_drop, habit = can_modify_habit(request, habit_id)

    if not can_drop:
        # report error
        return HttpResponse("you can't drop this habit")
    else:
        # drop
        drop_habit(habit)
        message = "droped habit " + str(habit_id)
        context = {'message': message}
        return render(request, 'tracker/drop_habit.html', context)


def drop_habit(habit):
    habit.delete()


def get_last_order(user):
    last_habit = Habit.objects.filter(user=user).order_by('order').last()
    if last_habit == None:
        return 1
    else:
        return last_habit.order + 1


@login_required
def edit_habit_controller(request, habit_id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddHabitForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = request.user

            # process the data in form.cleaned_data as required
            f = form.cleaned_data
            h = get_object_or_404(Habit, pk=habit_id)
            h.habit_name = f['habit_name']
            h.repetitions_per_week = f['repetitions_per_week']
            h.volume_with_units = f['volume_with_units']

            h.save()

            # redirect to a new URL:
            # i.e. return HttpResponseRedirect('/thanks/')
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        habit = get_object_or_404(Habit, pk=habit_id)
        form = AddHabitForm(initial={
            'habit_name': habit.habit_name,
            'repetitions_per_week': habit.repetitions_per_week,
            'volume_with_units': habit.volume_with_units,
        })
        context = {'form': form,
                   'habit_id': habit_id}

    return render(request, 'tracker/edit_habit.html', context)


@login_required
def add_habit_controller(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddHabitForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = request.user

            # process the data in form.cleaned_data as required
            f = form.cleaned_data
            h = Habit()
            h.habit_name = f['habit_name']
            h.repetitions_per_week = f['repetitions_per_week']
            h.volume_with_units = f['volume_with_units']

            h.starting_date = now()
            h.order = get_last_order(user)
            h.user = user

            h.save()

            # redirect to a new URL:
            # i.e. return HttpResponseRedirect('/thanks/')
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddHabitForm(initial={
            'habit_name': '',
            'repetitions_per_week': '7',
            'volume_with_units': ''
        })

    return render(request, 'tracker/add_habit.html', {'form': form})


def get_date_n_days_ago(n):
    '''
    Return the date n days ago
    :param n: number of days to go in past
    :return: date for that day
    '''
    time = now() - timezone.timedelta(days=n)
    return time


@login_required
def edit_record_controller(request, habit_id, number):
    n = int(number)
    habit = get_object_or_404(Habit, pk=habit_id)
    date = get_date_n_days_ago(n)

    # protect changing fields before starting_date
    if date_lt(date, habit.starting_date):
        return HttpResponse("can't add record for past yet")

    record = habit.get_record(date)
    if record == None:
        # create new record
        record_date = now() - timezone.timedelta(days=n)
        r = Record(habit=habit, date=record_date)
        r.save()
    else:
        # delete record
        record.delete()
    return redirect('tracker:mainpage')


def resetdb(request):
    User.objects.all().delete()
    u1 = User.objects.create_user(username=DEFAULT_USER, password="pass")
    u2 = User.objects.create_user(username="kaisa", password="pass")
    u3 = User.objects.create_user(username="pavel", password="pass")

    h1 = Habit(habit_name="run", repetitions_per_week=3, starting_date=now()-timezone.timedelta(days=20), volume_with_units="10 min", user=u1, order=1)
    h2 = Habit(habit_name="eat", repetitions_per_week=7, starting_date=now()-timezone.timedelta(days=3), volume_with_units="an apple", user=u2, order=2)
    h3 = Habit(habit_name="code", repetitions_per_week=7, starting_date=now()-timezone.timedelta(days=3), volume_with_units="1h", user=u2, order=1)
    h1.save()
    h2.save()
    h3.save()
    no_users = len(User.objects.all())
    no_habits = len(Habit.objects.all())

    r1 = Record(habit=h1, date=now())
    r2 = Record(habit=h1, date=now() - timezone.timedelta(days=5))
    r3 = Record(habit=h1, date=now() - timezone.timedelta(days=6))
    r4 = Record(habit=h1, date=now() - timezone.timedelta(days=8))
    r1.save()
    r2.save()
    r3.save()
    r4.save()

    message = "Database reseted with initial data. New " + str(no_users) + " users and new " + str(no_habits) + " habits"
    context = {'message': message}
    return render(request, 'tracker/resetdb.html', context)
