from django.shortcuts import render
from pip_files.filter_posts import *
from django.http import HttpResponseRedirect
import json

# feed page


def feed(request):

    # redirect to feed page if user is logged in
    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    if log_user_data['mode'] == 'prof':
        mode = 'Professional'

    if log_user_data['mode'] == 'edu':
        mode = 'Educational'

    if log_user_data['mode'] == 'per':
        mode = 'Personal'

    if log_user_data['username'] != '':
        if log_user_data['mode'] == 'prof':
            user_priority = log_user_data['user_priority_prof']
        if log_user_data['mode'] == 'edu':
            user_priority = log_user_data['user_priority_edu']
        if log_user_data['mode'] == 'per':
            user_priority = log_user_data['user_priority_per']
        posts = get_filt_posts(user_priority)
        return render(request, 'feed.html', {'all_post': posts, 'username': log_user_data['username'], 'mode': mode})
    else:
        return HttpResponseRedirect('/home/')

#to print the searched feed

def srch_feed(request,username_priority):

    # redirect to feed page if user is logged in
    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    mode = 'Results'

    if log_user_data['username'] != '':
        if username_priority == '':
            if log_user_data['mode'] == 'prof':
                user_priority = log_user_data['user_priority_prof']
            if log_user_data['mode'] == 'edu':
                user_priority = log_user_data['user_priority_edu']
            if log_user_data['mode'] == 'per':
                user_priority = log_user_data['user_priority_per']
        else:
            user_priority = [username_priority]
        posts = get_filt_posts(user_priority)
        return render(request, 'feed.html', {'all_post': posts, 'username': log_user_data['username'], 'mode': mode})
    else:
        return HttpResponseRedirect('/home/')

# logout user and change logged in user details to default

def logout(request):

    logout_usr_data = {
        'username': '',
        'password': '',
        'name': '',
        'email': '',
        'user_priority_prof': [],
        'user_priority_edu': [],
        'user_priority_per': [],
        'mode': '',
        'dob': '',
        'status': '',
        'about': ''
    }

    with open('database/logged_user.json', 'w') as log_user:
        json.dump(logout_usr_data, log_user, indent=2)

    return HttpResponseRedirect('/home/')

# setting page


def settings(request):

    # redirect to setting page user if logged in and home page if user is logged out
    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    with open('database/profiles_database.json') as prf_db:
        profile_data = json.load(prf_db)

    user_priority = 'user_priority_' + log_user_data['mode']

    if log_user_data['mode'] == 'prof':
        mode = 'Professional'

    if log_user_data['mode'] == 'edu':
        mode = 'Educational'

    if log_user_data['mode'] == 'per':
        mode = 'Personal'

    if log_user_data['username'] != '':
        if log_user_data['First_login'] :
            title = 'Setup'
            log_user_data['First_login'] = False
            profile_data['profiles'][log_user_data['username']]['First_login'] = False
            with open('database/logged_user.json', 'w') as log_user:
                json.dump(log_user_data, log_user, indent=2)

            with open('database/profiles_database.json', 'w') as prf_db:
                json.dump(profile_data, prf_db, indent=2)

        else:
            title = 'Settings'

        attrs = {
                'user_priority': log_user_data[user_priority],
                 'username': log_user_data['username'], 
                 'mode': mode, 
                 'name' : log_user_data['name'],
                 'about': log_user_data['about'],
                 'status' : log_user_data['status'],
                 'dob' : log_user_data['dob'],
                 'title' : title  
                 }
        return render(request, 'settings.html', attrs)
    else:
        return HttpResponseRedirect('/home/')

# to add new user in user priority list


def loading(request):
    return render(request, 'loading.html')

def add_user(request):

    # add new user in user priority list of user_profile database and logged in user data
    # redirect to back setting page user if logged in and home page if user is logged out
    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    with open('database/profiles_database.json') as prf_db:
        profile_data = json.load(prf_db)

    user_priority = 'user_priority_' + log_user_data['mode']

    if log_user_data['username'] != '':

        new_user = request.POST['new_user']

        if new_user != '' and new_user not in log_user_data[user_priority]:
            log_user_data[user_priority].append(new_user)
            profile_data['profiles'][log_user_data['username']
                                     ][user_priority].append(new_user)

            with open('database/logged_user.json', 'w') as log_user:
                json.dump(log_user_data, log_user, indent=2)

            with open('database/profiles_database.json', 'w') as prf_db:
                json.dump(profile_data, prf_db, indent=2)

        return HttpResponseRedirect('/settings/')
    else:
        return HttpResponseRedirect('/home/')

# to delete new user in user priority list


def del_user(request, user_name):

    # add new user in user priority list from user_profile database and logged in user data
    # redirect to back setting page user if logged in and home page if user is logged out
    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    with open('database/profiles_database.json') as prf_db:
        profile_data = json.load(prf_db)

    user_priority = 'user_priority_' + log_user_data['mode']

    if log_user_data['username'] != '':

        if user_name != '' and user_name in log_user_data[user_priority]:
            log_user_data[user_priority].remove(user_name)
            profile_data['profiles'][log_user_data['username']
                                     ][user_priority].remove(user_name)

            with open('database/logged_user.json', 'w') as log_user:
                json.dump(log_user_data, log_user, indent=2)

            with open('database/profiles_database.json', 'w') as prf_db:
                json.dump(profile_data, prf_db, indent=2)

        return HttpResponseRedirect('/settings/')
    else:
        return HttpResponseRedirect('/home/')

# search engine


def search(request):

    username = request.POST['username']
    #to check the type of search
    #to redirect to feed of searched username
    if username[0] == '!' and len(username)>1:
        url = '/srch_feed/'+username[1:]+'/'
        return HttpResponseRedirect(url)
    else:    
    # to redirect to user profile url
        url = '/profile/'+username+'/'
        return HttpResponseRedirect(url)

# user profile managment


def user_profile(request, username):

    with open('database/profiles_database.json') as prf_db:
        profile_data = json.load(prf_db)

    # to check reqired user exists
    # redirect to user profile  if exists and redirect to same page if not
    if username in profile_data['profiles']:
        return render(request, 'user_profile.html', {'user_profile': profile_data['profiles'][username], 'username': username})

    else:
        return HttpResponseRedirect('/loading/')


def setting_chng(request):
    name = request.POST['name']
    dob = request.POST['DOB']
    status = request.POST['status']
    about = request.POST['about']

    # to update the data in user_profile data base and logged in user data if data is provided
    # if not provided no change will happen
    with open('database/profiles_database.json') as prf_db:
        profile_data = json.load(prf_db)

    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    # name updata
    if name != '':
        profile_data['profiles'][log_user_data['username']]['name'] = name
        log_user_data['name'] = name

    # date of birth update
    if dob != '':
        profile_data['profiles'][log_user_data['username']]['dob'] = dob
        log_user_data['dob'] = dob

    # status update
    if status != '':
        profile_data['profiles'][log_user_data['username']]['status'] = status
        log_user_data['status'] = status

    if about != '':
        profile_data['profiles'][log_user_data['username']]['about'] = about
        log_user_data['about'] = about

    with open('database/logged_user.json', 'w') as log_user:
        json.dump(log_user_data, log_user, indent=2)

    with open('database/profiles_database.json', 'w') as prf_db:
        json.dump(profile_data, prf_db, indent=2)

    # redirect back to settings
    return HttpResponseRedirect('/settings/')


def mode_prof(request):
    with open('database/profiles_database.json') as prf_db:
        profile_data = json.load(prf_db)

    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    profile_data['profiles'][log_user_data['username']]['mode'] = 'prof'
    log_user_data['mode'] = 'prof'

    with open('database/logged_user.json', 'w') as log_user:
        json.dump(log_user_data, log_user, indent=2)

    with open('database/profiles_database.json', 'w') as prf_db:
        json.dump(profile_data, prf_db, indent=2)

    # redirect back to settings
    return HttpResponseRedirect('/settings/')


def mode_edu(request):
    with open('database/profiles_database.json') as prf_db:
        profile_data = json.load(prf_db)

    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    profile_data['profiles'][log_user_data['username']]['mode'] = 'edu'
    log_user_data['mode'] = 'edu'

    with open('database/logged_user.json', 'w') as log_user:
        json.dump(log_user_data, log_user, indent=2)

    with open('database/profiles_database.json', 'w') as prf_db:
        json.dump(profile_data, prf_db, indent=2)

    # redirect back to settings
    return HttpResponseRedirect('/settings/')


def mode_per(request):
    with open('database/profiles_database.json') as prf_db:
        profile_data = json.load(prf_db)

    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    profile_data['profiles'][log_user_data['username']]['mode'] = 'per'
    log_user_data['mode'] = 'per'

    with open('database/logged_user.json', 'w') as log_user:
        json.dump(log_user_data, log_user, indent=2)

    with open('database/profiles_database.json', 'w') as prf_db:
        json.dump(profile_data, prf_db, indent=2)

    # redirect back to settings
    return HttpResponseRedirect('/settings/')