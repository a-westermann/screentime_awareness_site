from django.shortcuts import render
from django.http import HttpResponse
from screentime_awareness.helpers import security
from django.urls import reverse


def index(request):
    reverse('screentime_awareness.views.log_in', 'asdef', 'asdfk')
    context = {'secret': security.get_secret()}
    # pw = 'Apostria1!'
    # security.encrypt_pw('adw8122', pw)
    # print(f"pw {pw} valid: {security.validate_pw('adw8122', pw)}")
    return render(request, 'screentime_awareness/index.html', context=context)

def log_in(request, user_id: str, pw: str):
    if security.validate_pw(user_id, pw):
        print('success')
        return render(request, 'screentime_awareness/account.html')
    else:
        print('fail')
        return render(request, 'screentime_awareness/index.html')

def account(request):
    return render(request, 'screentime_awareness/account.html')

def learn_more(request):
    return render(request, 'screentime_awareness/learn_more.html')

def donate(request):
    return render(request, 'screentime_awareness/donate.html')
