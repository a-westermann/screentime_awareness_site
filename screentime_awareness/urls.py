from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account', views.account, name='account'),
    path('learnmore', views.learn_more, name='learn_more'),
    path('donate', views.donate, name='donate')
]