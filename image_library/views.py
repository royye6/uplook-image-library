from django.shortcuts import render, redirect
import requests, environ, os, json
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pexelsapi.pexels import Pexels

@login_required(login_url='login')
def index(request):
    access_key = os.environ.get('PEXELS_KEY')

    if not access_key:
        raise KeyError('Pexels access key not found in environment variables')
    
    search_term = request.GET.get('search_term')
    if search_term:
        per_page = 80
        page = 1
        url = f'https://api.pexels.com/v1/search?query={search_term}&per_page={per_page}&orientation=landscape'

        headers = {"Authorization": f"{access_key}"}
        response=requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(data)
            photos = data['photos']
            return render(request, 'index.html', context={'photos': photos})
        else:
            data = None
            print(f"Error: {response.status_code}")
            messages.info(request, f'API request failed (status code: {response.status_code})')
    else:
        photos = []

    return render(request, 'index.html', context={'photos': photos})


# def index(request):
#     return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if username != '' and email != '' and password != '' and password2 != '':
            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('register')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username is taken')
                    return redirect('register')
                else:
                    # when all checks pass
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save() 

                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)
                    return redirect('/')
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
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username != '' and password != '':
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Incorrect username or password')
                return redirect('login') 
        else:
            messages.info(request, 'Please fill in all the required fields')
            return redirect('login')

    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')

