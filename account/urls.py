from django.urls import path, include
from . import admin,views

#from account import admin
from django.conf.urls import url
from django.conf import settings #add this
from django.conf.urls.static import static #add this

urlpatterns = [
    path('',views.home,name="home"),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    
]