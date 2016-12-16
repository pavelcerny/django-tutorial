from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse


def resetdb(request):
    User.objects.all().delete()
    user = User.objects.create_user(username="pavel",password="pass")

    return HttpResponse("delete db and prepopulate db with default users")


def log_in(request):
    username = 'pavel'
    password = 'pass'
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect(reverse('users:loged'))
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("log uncorrect")


def loged(request):
    return HttpResponse(request.user.username + ", you are loged in")