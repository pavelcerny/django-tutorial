from django.db import models
from django.utils import timezone


class User(models.Model):
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.user_name


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit_name = models.CharField(max_length=200)
    repetitions_per_week = models.IntegerField(default=7)
    volume_with_units = models.CharField(max_length=200)
    starting_date = models.DateTimeField('date_started')
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.habit_name + " " + str(self.repetitions_per_week) + " " + self.volume_with_units

    def get_table_of_records(self,number):
        return [0] * number


class Record(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateTimeField('date_recorded')

    def __str__(self):
        return self.habit.habit_name + " on " + str(self.date.date())




