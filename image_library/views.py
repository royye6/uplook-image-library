from django.shortcuts import render
import requests, environ, os, json


def index(request):
    access_key = os.environ.get('ACCESS_KEY')

    if not access_key:
        raise ValueError('Access key not found in environment variables')
    
    if request.method == 'GET':
        search_term = request.GET.get('search_term')
        url = f'https://api.unsplash.com/search/photos?client_id={access_key}&query={search_term}'
        response=requests.get(url)

    if response.status_code == 200:
        print(response.json())
        return render(request, 'index.html', context={'unsplash_data': response.json()})
    else:
        return render(request, 'index.html', context={'error': 'API request failed'})


# def index(request):
#     return render(request, 'index.html')

