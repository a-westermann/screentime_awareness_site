from django.shortcuts import render
from django.http import HttpResponse
from screentime_awareness.helpers import security, db, member_communication
from django.shortcuts import redirect
from screentime_awareness.models import User
import json
import sys


def index(request, invalid_login=False, logout=False):
    # ip = requests.get('https://checkip.amazonaws.com')
    # print(ip)
    context = {}
    if 'runserver' in sys.argv:
        context['dev'] = True
    if logout and request.session and 'user' in request.session:
        print('logging out')
        request.session.clear()
    if request.session and 'user' in request.session and request.session['user']\
            and json.loads(request.session['user']):
        return redirect('home')
    else:
        context['logged_out'] = True
    if invalid_login:
        context['invalid_login'] = True
    return render(request, 'screentime_awareness/index.html', context=context)

def home(request):
    if not request.session or 'user' not in request.session or not request.session['user']:
        # user is not logged in this session. Redirect to index
        return redirect('index')
    username = json.loads(request.session['user'])['username']
    context = {'username': username}
    if 'runserver' in sys.argv:
        context['dev'] = True
    return render(request, 'screentime_awareness/home.html', context=context)


#<editor-fold desc="Registration and Login">
def log_in_user(request):
    # This method is called to try to log in a user when they submit their credentials
    # Upon success, it redirects them to the home page
    # Failure reloads the login page for them to try again, and displays info about the failed login attempt
    if request.POST:
        email_or_username = request.POST.get('email_address_username', None)
        pw = request.POST.get('pw', None)
        user = security.get_user(email_or_username, pw)
        if not email_or_username or not pw or not user:
            return redirect('index', invalid_login=True)
        else:  # valid login. Redirect to home
            # set up a User object to save the user's information to the session
            request.session['user'] = user.to_json()
            request.session.save()
            return redirect('home')
            # return render(request, 'screentime_awareness/home.html')
    else:
        print('failed to get post data from login form')

def register(request, invalid_creds=False, already_registered=False,
             bad_chars=False):
    context = {}
    if invalid_creds:
        context['invalid_creds'] = True
    elif already_registered:
        context['already_registered'] = True
    elif bad_chars:
        context['bad_chars'] = True
    return render(request, 'screentime_awareness/register.html', context=context)

def register_user(request):
    if request.POST:
        email = request.POST.get('email_address', None)
        # if the email is already registered, deny
        if security.check_registered(email):
            return redirect('register', already_registered=True)
        username = request.POST.get('username', None)
        pw = request.POST.get('pw', None)
        confirm_pw = request.POST.get('confirm_pw', None)
        # validate email and password. If invalid, reload register.html
        if not email or not username or not pw or pw != confirm_pw:
            return redirect('register', invalid_creds=True)
        elif security.bad_creds_chars(username + pw):
            return redirect('register', bad_chars=True)
        # if valid, update the db and direct them to home
        else:
            security.add_user_to_db(email, pw, username)
            user = User(email, username)
            request.session['user'] = user.to_json()
            request.session.save()
            return render(request, 'screentime_awareness/home.html')
    else:
        print('error')

def forgot_pw(request, not_found=False, sent_recovery=False):
    context = {
        'not_found': not_found,
        'sent_recovery': sent_recovery
    }
    return render(request, 'screentime_awareness/forgot_password.html', context=context)

def forgot_pw_submit(request):
    if request.POST:
        email_user = request.POST.get('email_username', None)
        if not email_user:
            return redirect('forgot_pw', not_found=True)
        user = security.get_user(email_user, '', ignore_pw=True)
        if not user:
            return redirect('forgot_pw', not_found=True)
        member_communication.email_pw_recovery(user.email)
        return redirect('forgot_pw', sent_recovery=True)

def reset_pw(request, uid='', reset_complete=False):
    context = {}
    if not reset_complete:
        # check if there is a password reset record for the entered uid
        print(f'reset uid = {uid}')
        email = security.reset_pw(uid)
        print(f'reset emaiL:  {email}')
        if email:
            request.session['reset_pw_found_email'] = email
        else:
            context['invalid_link'] = True
            print('invalid reset link')
    else:
        context['reset_success'] = reset_complete
        # update the user's password after checking validity
        pw = request.POST.get('pw', None)
        confirm_pw = request.POST.get('confirm_pw', None)
        if not pw or pw != confirm_pw or security.bad_creds_chars(pw):
            context['invalid_pw'] = True
        else:
            security.update_pw(request.POST.get('pw'), request.session['reset_pw_found_email'])
    return render(request, 'screentime_awareness/reset_pw.html', context=context)

#</editor-fold>

def account(request):
    return render(request, 'screentime_awareness/account.html')


def activities(request):
    # Should I make a new DBC instance every time I need one? Or use a singleton paradigm?
    # What would a singleton do for multiple users being logged in at once?
    dbc = db.DBC()
    printables = dbc.select("select * from activities where activity_type = 'printable'")
    ideas = dbc.select("select * from activities where activity_type = 'idea'")
    context = {
        'printables': printables,
        'ideas': ideas,
    }
    return render(request, 'screentime_awareness/activities.html', context=context)

def learn_more(request):
    context = {}
    if not request.session or 'user' not in request.session or not request.session['user']:
        context['logged_out_learn_more'] = True
    return render(request, 'screentime_awareness/learn_more.html', context=context)

def donate(request):
    return render(request, 'screentime_awareness/donate.html')


# dnd - each shop has a link, no index page. That way I can only give them the menus as I want
# Could I just have 1 view that looks up the shop name based on the url?
def ember(request):
    dbc = db.DBC()
    try:
        inventory = dbc.select("select * from shop_inventories where shop = 'ember_and_ink' limit 1",)
        context = {'items': inventory}
    except SystemError as e:
        context = {'items': e}
    return render(request, 'dnd/ember.html', context=context)

