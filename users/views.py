from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def resetdb(request):
    User.objects.all().delete()
    user = User.objects.create_user(username="pavel",password="pass")

    return HttpResponse("delete db and prepopulate db with default users")


def log_out(request):
    logout(request)

    return HttpResponseRedirect(reverse('users:logedout'))


@login_required
def loged(request):
    context = {'username': request.user.username }
    return render(request, 'users/loged.html', context)


def logedout(request):
    return render(request, 'users/logedout.html')