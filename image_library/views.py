from django.shortcuts import render, redirect
import requests, environ, os, json
from django.contrib.auth.models import User, auth
from django.contrib import messages
from pexels_api import Api


def index(request):
    access_key = os.environ.get('ACCESS_KEY')

    if not access_key:
        raise ValueError('Access key not found in environment variables')
    
    search_term = request.GET.get('search_term')
    if search_term:
        client = Api(access_key)
        response = client.get_photos(query=search_term, per_page=1, page=1)
        
        if response.success:
            photos = response.photos
            context = {'photos': photos}
            print(response)
            return render(request, 'index.html', context)
       
        else:
            error_message = response.errors[0]['message']
            context = {'error_message': error_message}
            print("error_message")
            messages.info(request, 'API data not retrieved')
            return render(request, 'index.html', context)
    else:
        context = {None}
        return render(request, 'index.html', context)


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
                    return redirect('profile')
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
                return redirect('profile')
            else:
                messages.info(request, 'Incorrect username or password')
                return redirect('login') 
        else:
            messages.info(request, 'Please fill in all the required fields')
            return redirect('login')

    else:
        return render(request, 'login.html')


def profile(request):
    return render(request, 'profile.html')

