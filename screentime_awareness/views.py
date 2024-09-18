from django.shortcuts import render
from django.http import HttpResponse
from screentime_awareness.helpers import security


def index(request):
    context = {'secret': security.get_secret()}
    security.encrypt_pw('adw8122', 'Apostria1!')
    return render(request, 'screentime_awareness/index.html', context=context)

def learn_more(request):
    return render(request, 'screentime_awareness/learn_more.html')

def donate(request):
    return render(request, 'screentime_awareness/donate.html')