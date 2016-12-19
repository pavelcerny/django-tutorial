from django import forms
from django.utils import timezone

class AddHabitForm(forms.Form):
    habit_name = forms.CharField(label='Habit name', max_length=200)
    repetitions_per_week = forms.IntegerField(initial=7)
