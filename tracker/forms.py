from django import forms
from django.utils import timezone

class AddHabitForm(forms.Form):
    habit_name = forms.CharField(label='Habit name', max_length=200)
    volume_with_units = forms.CharField(max_length=200)
    repetitions_per_week = forms.IntegerField(initial=7)
    starting_date = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now())
    order = forms.IntegerField(widget=forms.HiddenInput(),initial=1)

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
