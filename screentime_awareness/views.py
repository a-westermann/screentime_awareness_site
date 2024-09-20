from django.shortcuts import render
from django.http import HttpResponse
from screentime_awareness.helpers import security
from django.urls import reverse


def index(request):
    return render(request, 'screentime_awareness/index.html')

def account(request):
    if request.POST:
        email_address = request.POST.get('email_address', None)
        pw = request.POST.get('pw', None)
        if not email_address or not pw or not security.validate_pw(email_address, pw):
            context = {'invalid_login': True}
            #TODO: Forgot password here
            return render(request, 'screentime_awareness/index.html', context=context)
        else:  # valid login. Redirect to account center
            # pass username? create a user object?
            return render(request, 'screentime_awareness/account.html')
    else:
        print('failed to get post data from login form')


def learn_more(request):
    return render(request, 'screentime_awareness/learn_more.html')

def donate(request):
    return render(request, 'screentime_awareness/donate.html')
