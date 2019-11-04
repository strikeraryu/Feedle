"""Feedle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login_sys.views import home, sign_up, reg_user, login, validate
from profile_sys.views import feed, logout, settings, setting_chng, add_user, del_user, search, user_profile, mode_prof, mode_edu, mode_per, loading, srch_feed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home/', home),
    path('sign_up/', sign_up),
    path('login/', login),
    path('reg/', reg_user),
    path('valid/', validate),
    path('loading/', loading),
    path('feed/', feed),
    path('srch_feed/<str:username_priority>/', srch_feed),
    path('logout/', logout),
    path('settings/', settings),
    path('setting_chng/', setting_chng),
    path('mode_prof/', mode_prof),
    path('mode_edu/', mode_edu),
    path('mode_per/', mode_per),
    path('add_user/', add_user),
    path('del_user/<str:user_name>/', del_user),
    path('search/', search),
    path('profile/<str:username>/', user_profile)
]
