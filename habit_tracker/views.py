from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("hello world from habit tracker")


def statistics(request):
    return HttpResponse("statistics page")


def about(request):
    return HttpResponse("about page")
