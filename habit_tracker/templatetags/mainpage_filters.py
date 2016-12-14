from django import template
from habit_tracker.views import HabitItem

register = template.Library()


@register.filter
def speed_in_percent(speed):
    # call some code
    percentage = int(round(speed * 100,0))
    return str(percentage) + " %"


@register.filter
def name_formated(habit_item):
    name = habit_item.habit.habit_name
    amount = habit_item.habit.volume_with_units
    return name + " " + amount


