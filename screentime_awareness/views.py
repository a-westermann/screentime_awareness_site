from django.shortcuts import render
from django.http import HttpResponse
from screentime_awareness.helpers import security
from django.shortcuts import redirect


def index(request, invalid_login=False):
    context = {}
    if invalid_login:
        # TODO: Forgot password added
        context['invalid_login'] = True
    return render(request, 'screentime_awareness/index.html', context=context)

def home(request):
    context = {}
    return render(request, 'screentime_awareness/home.html', context=context)

def account(request):
    if request.POST:
        email_address = request.POST.get('email_address', None)
        pw = request.POST.get('pw', None)
        if not email_address or not pw or not security.validate_pw(email_address, pw):
            return redirect('index', invalid_login=True)
        else:  # valid login. Redirect to account center
            # pass username? create a user object?
            return render(request, 'screentime_awareness/account.html')
    else:
        print('failed to get post data from login form')

def register(request, invalid_creds=False):
    context = {}
    if invalid_creds:
        context['invalid_creds'] = True
    return render(request, 'screentime_awareness/register.html', context=context)

def register_user(request):
    if request.POST:
        email = request.POST.get('email_address', None)
        pw = request.POST.get('pw', None)
        confirm_pw = request.POST.get('confirm_pw', None)
        # validate email and password. If invalid, reload register.html
        if not email or not pw or pw != confirm_pw:
            return redirect('register', invalid_creds=True)
        # if valid, update the db and direct them to home
        else:
            security.add_user_to_db(email, pw)
            return render(request, 'screentime_awareness/home.html')
    else:
        print('error')

def learn_more(request):
    return render(request, 'screentime_awareness/learn_more.html')

def donate(request):
    return render(request, 'screentime_awareness/donate.html')
