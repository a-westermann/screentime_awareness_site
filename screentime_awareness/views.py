from django.shortcuts import render
from django.http import HttpResponse
from screentime_awareness.helpers import security
from django.shortcuts import redirect
from  screentime_awareness.models import User


def index(request, invalid_login=False):
    context = {}
    if invalid_login:
        # TODO: Forgot password added
        context['invalid_login'] = True
    return render(request, 'screentime_awareness/index.html', context=context)

def home(request):
    if not request.session or 'user' not in request.session:
        # user is not logged in this session. Redirect to index
        return redirect('index')
    context = {'username': request.session['user'].username}
    return render(request, 'screentime_awareness/home.html', context=context)

def log_in_user(request):
    # This method is called to try to log in a user when they submit their credentials
    # Upon success, it redirects them to the home page
    # Failure reloads the login page for them to try again, and displays info about the failed login attempt
    if request.POST:
        email_address = request.POST.get('email_address', None)
        pw = request.POST.get('pw', None)
        user = security.get_user(email_address, pw)
        if not email_address or not pw or not user:
            return redirect('index', invalid_login=True)
        else:  # valid login. Redirect to home
            # set up a User model to save the user's information for this session
            request.session['user'] = user.to_json()
            return render(request, 'screentime_awareness/home.html')
    else:
        print('failed to get post data from login form')

def register(request, invalid_creds=False, already_registerd=False):
    context = {}
    if invalid_creds:
        context['invalid_creds'] = True
    elif already_registerd:
        context['already_registered'] = True
    return render(request, 'screentime_awareness/register.html', context=context)

def register_user(request):
    if request.POST:
        email = request.POST.get('email_address', None)
        # if the email is already registered, deny
        if security.check_registered(email):
            return redirect('register', already_registered=True)
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

def account(request):
    return render(request, 'screentime_awareness/account.html')

def learn_more(request):
    return render(request, 'screentime_awareness/learn_more.html')

def donate(request):
    return render(request, 'screentime_awareness/donate.html')
