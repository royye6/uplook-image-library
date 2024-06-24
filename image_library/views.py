from django.shortcuts import render, redirect
import requests, environ, os, json
from django.contrib.auth.models import User, auth
from django.contrib import messages

def index(request):
    access_key = os.environ.get('ACCESS_KEY')

    if not access_key:
        raise ValueError('Access key not found in environment variables')
    
    if request.method == 'GET':
        search_term = request.GET.get('search_term')
        per_page = 1
        url = f'https://api.unsplash.com/search/photos?client_id={access_key}&query={search_term}&per_page={per_page}&page=1'
        response=requests.get(url)

    if response.status_code == 200:
        print(response.json())
        return render(request, 'index.html', context={'unsplash_data': response.json()})
    else:
        return render(request, 'index.html', context={'error': 'API request failed'})


# def index(request):
#     return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if username != None and email != None and password != None and password2 != None:
            if password == password2:
                if User.objects.filter(email=email).exists:
                    messages.info(request, 'Email already exists')
                    return redirect('register')
                elif User.objects.filter(username=username):
                    messages.info(request, 'Username is taken')
                    return redirect('register')
                else:
                    # when all checks pass
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save() 

                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)
                    return redirect('profile.html')
            else:
                messages.info(request, 'Passwords do not match')
                return redirect('register')
        else:
            messages.info(request, 'Please fill in all the required fields')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        pass
    return render(request, 'login.html')


def profile(request):
    return render(request, 'profile.html')

