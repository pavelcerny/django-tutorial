from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

def resetdb(request):
    User.objects.all().delete()
    user = User(first_name="Pavel",password="pass")

    return HttpResponse("delete db and prepopulate db with default users")