from django import forms
from django.utils import timezone

class AddHabitForm(forms.Form):
    habit_name = forms.CharField(label='Habit name', max_length=200)
    repetitions_per_week = forms.IntegerField(initial=7)


class ChangeOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super().__init__(*args, **kwargs)

        for habit_id, order in extra:
            self.fields['%s' % habit_id] = forms.IntegerField(initial=order)

    def get_answers(self):
        return self.cleaned_data
