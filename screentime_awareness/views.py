from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'screentime_awareness/index.html')

def learn_more(request):
    return render(request, 'screentime_awareness/learn_more.html')