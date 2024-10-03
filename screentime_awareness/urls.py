from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path(r'^(?P<uid=>[0-9]+)/$', views.index, name='index'),
    path('invalid_login=<invalid_login>/', views.index, name='index'),
    path('logout=<logout>/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('log_in_user/', views.log_in_user, name='log_in_user'),
    path('register/', views.register, name='register'),
    path('register_user/', views.register_user, name='register_user'),
    path('register/invalid_creds=<invalid_creds>/', views.register, name='register'),
    path('register/already_registered=<already_registered>/', views.register, name='register'),
    path('register/bad_chars=<bad_chars>/', views.register, name='register'),
    path('forgot_pw/', views.forgot_pw, name='forgot_pw'),
    path('forgot_pw/not_found=<not_found>/', views.forgot_pw, name='forgot_pw'),
    path('forgot_pw/sent_recovery=<sent_recovery>/', views.forgot_pw, name='forgot_pw'),
    path('forgot_pw_submit', views.forgot_pw_submit, name='forgot_pw_submit'),
    # re_path(r'^(reset_pw/(?:(P<uid>[.*]))?(?:(P<reset_complete>(True|False))?))/$', views.reset_pw, name='reset_pw'),
    # re_path(r'^reset_pw/((?P<uid>.*)/)?(?P<reset_complete>(True|False))$', views.reset_pw, name='reset_pw'),
    re_path(r'reset_pw/uid=(?P<uid>.*?)/?$', views.reset_pw, name='reset_pw'),
    # re_path(r'reset_pw/(?P<reset_complete>.*?)/?$', views.reset_pw, name='reset_pw'),
    path('reset_pw/reset_complete=<reset_complete>/', views.reset_pw, name='reset_pw'),
    path('activities/', views.activities, name='activities'),
    path('learnmore/', views.learn_more, name='learn_more'),
    path('donate/', views.donate, name='donate')
]