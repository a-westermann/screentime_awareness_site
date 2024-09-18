from django.shortcuts import render
from django.http import HttpResponse
from helpers import security


def index(request):
    context = {'secret': security.get_secret()}
    return render(request, 'screentime_awareness/index.html')

def learn_more(request):
    return render(request, 'screentime_awareness/learn_more.html')

def donate(request):
    return render(request, 'screentime_awareness/donate.html')