from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'invalid_login=<invalid_login>', views.index, name='index'),
    path('home', views.home, name='home'),
    path('account', views.log_in_user, name='account'),
    path('log_in_user', views.log_in_user, name='log_in_user'),
    path('register', views.register, name='register'),
    path('register_user', views.register_user, name='register_user'),
    path('register/invalid_creds=<invalid_creds>', views.register, name='register'),
    path('learnmore', views.learn_more, name='learn_more'),
    path('donate', views.donate, name='donate')
]