import datetime
from django.db import models
from django.utils import timezone

# to change models:
# https://docs.djangoproject.com/en/1.10/intro/tutorial02/#activating-models
#  1) Change your models (in models.py).
#  2) Run python manage.py makemigrations to create migrations for those changes
#  3) Run python manage.py migrate to apply those changes to the database.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    # my own function
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
