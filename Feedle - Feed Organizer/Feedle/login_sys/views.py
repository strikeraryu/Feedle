from django.shortcuts import render
from django.http import HttpResponseRedirect
from pip_files.encode import *
import json


# home page
def home(request):
    # to check if user logged in or not
    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    # redirect to profile if logged in
    if log_user_data['username'] != '':
        return HttpResponseRedirect('/loading/')
    else:
        return render(request, 'home.html')

# sign up page


def sign_up(request):
    # to check if user logged in or not
    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    # redirect to profile if logged in
    if log_user_data['username'] != '':
        return HttpResponseRedirect('/loading/')
    else:
        return render(request, 'sign_up.html')
# login page


def login(request):
    # to check if user logged in or not
    with open('database/logged_user.json') as log_user:
        log_user_data = json.load(log_user)

    # redirect to profile if logged in
    if log_user_data['username'] != '':
        return HttpResponseRedirect('/loading/')
    else:
        return render(request, 'login.html')

# to register new user


def reg_user(request):

    # to take data from the website
    reg_name = request.POST['name']
    reg_username = request.POST['username']
    reg_email = request.POST['email']
    reg_password = request.POST['password']

    with open('database/user_database.json') as usr_db:
        user_data = json.load(usr_db)

    with open('database/profiles_database.json') as prf_db:
        profile_data = json.load(prf_db)

    new_usr = True

    # to check already existing username
    for user in user_data['users']:
        if reg_username in user:
            new_usr = False
            break

    if new_usr:
        # to store login credentials of each user
        new_user_data = {
            reg_username: {
                'name': reg_name,
                'password': encrypt(reg_password),
                'email': reg_email
            }
        }

        user_data['users'].append(new_user_data)

        with open('database/user_database.json', 'w') as usr_db:
            json.dump(user_data, usr_db, indent=2)

        # to create default profile
        new_user_profile = {
            reg_username: {
                'password': encrypt(reg_password),
                'name': reg_name,
                'email': reg_email,
                'user_priority_prof': [],
                'user_priority_edu': [],
                'user_priority_per': [],
                'mode': 'prof',
                'dob': '',
                'status': 'Hey, I am new here',
                'about' : 'About',
                'First_login' : True
            }
        }

        profile_data['profiles'].update(new_user_profile)

        with open('database/profiles_database.json', 'w') as prf_db:
            json.dump(profile_data, prf_db, indent=2)

        return HttpResponseRedirect('/login/')

    # to redirect to signup page if username is already exists
    else:
        return render(request, 'sign_up.html', {'chk': 0})

# to verify login credentails


def validate(request):

    # to take data from the website
    log_username = request.POST['log_username']
    log_password = request.POST['log_password']

    valid = False
    new_usr = True

    with open('database/user_database.json') as usr_db:
        user_data = json.load(usr_db)

    with open('database/profiles_database.json') as prf_db:
        profile_data = json.load(prf_db)

    # to verify username exists
    for user in user_data['users']:
        if log_username in user:

            # to check the login credential is correct
            if decrypt(user[log_username]['password']) == log_password:
                valid = True

                # to store data of logged in user
                log_usr_data = {
                    'username': log_username,
                    'password': user[log_username]['password'],
                    'name': user[log_username]['name'],
                    'email': user[log_username]['email'],
                    'user_priority_prof': profile_data['profiles'][log_username]['user_priority_prof'],
                    'user_priority_edu': profile_data['profiles'][log_username]['user_priority_edu'],
                    'user_priority_per': profile_data['profiles'][log_username]['user_priority_per'],
                    'mode': profile_data['profiles'][log_username]['mode'],
                    'dob': profile_data['profiles'][log_username]['dob'],
                    'status': profile_data['profiles'][log_username]['status'],
                    'about' : profile_data['profiles'][log_username]['about'],
                    'First_login' : profile_data['profiles'][log_username]['First_login']
                }

                with open('database/logged_user.json', 'w') as log_usr:
                    json.dump(log_usr_data, log_usr, indent=2)
            new_usr = False
            break

    # redirect to feed page if login credentials is correct
    if not new_usr and valid:
        if profile_data['profiles'][log_username]['First_login']:
            return HttpResponseRedirect('/settings/')
        else:
            return HttpResponseRedirect('/loading/')

    # redirect to login page if user dont exists or wrong credentials
    else:
        return render(request, 'login.html', {'chk': 0})
