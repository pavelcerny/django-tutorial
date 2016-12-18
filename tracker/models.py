from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit_name = models.CharField(max_length=200)
    repetitions_per_week = models.IntegerField(default=7)
    volume_with_units = models.CharField(max_length=200)
    starting_date = models.DateField('date_started')
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.habit_name + " " + str(self.repetitions_per_week) + " " + self.volume_with_units

    def get_record(self, date):
        record = Record.objects.filter(
            habit=self,
            date__year=date.year,
            date__month=date.month,
            date__day=date.day
        ).first()
        return record


class Record(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField('date_recorded')

    def __str__(self):
        return self.habit.habit_name + " on " + str(self.date.date())




