import math
from django import template
from tracker.views import HabitItem, RecordValues
from django.utils import timezone

register = template.Library()


@register.filter
def ratio_to_percents(speed):
    # call some code
    percentage = int(round(speed * 100,0))
    return str(percentage) + " %"\


@register.filter
def ratio_to_grad(ratio):
    if ratio > 0.8:
        return "good"
    else:
        if ratio > 0.4:
            return "ok"
        else:
            return "bad"


@register.filter
def name_formated(habit_item):
    name = habit_item.habit.habit_name
    return name


@register.filter
def date_formated(date):
    day = str(date.day)
    month = str(date.month)
    year = str(date.year)

    today = timezone.now().date()
    if date == today:
        return "today"
    else:
        return day + "." + month

@register.filter()
def format_days_elapsed(date):
    days = date.days
    weeks = math.ceil(days/7)

    if days < 7:
        return str(days) + " days"
    else:
        return str(weeks) + " weeks"

@register.filter
def format_elapsed_time_statistics(date):
    days = str(date.days)
    return days

@register.filter
def render_checkbox(record):
    return 'checkbox'

@register.filter
def checkbox_state(record):
    if record == RecordValues.SUCCESS:
        return "true"
    else:
        return "false"
