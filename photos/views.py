from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache

import random


def photosHome(request, page=''):

    if page == '' or page == 'people' or page == 'places':
        try:
            photos = getCollection(page)

        except:
            photos = None

        return render(request, 'photos/index.html', { 'photos' : photos })

    else: return render(request, 'error404.html')


def getCollection(page):

    display = 30

    if page == 'people':
        photos = cache.get('flickr_people')

    elif page == 'places':
        photos = cache.get('flickr_places')

    else:
        photos = cache.get('flickr_latest')
        display = 15

    photos = photos[:display]
    return random.sample(photos, len(photos))


def photosRandom(request):

    photos = []

    if request.user.is_authenticated:
        photos = cache.get('flickr_random')

    else:
        photos = cache.get('flickr_faves')

    if len(photos) < 4:
        max = len(photos)

    else:
        max = 4

    photos = random.sample(photos, max)

    return render(request, 'photos/random.html', { 'photos' : photos, })


def photosRandomApi(request):

    if not request.GET.get('token'):
        return HttpResponse(status=404)

    elif request.GET.get('token') != settings.API_ACCESS_KEY:
        return HttpResponse(status=401)

    else:

        try:
            photo = random.sample(cache.get('flickr_faves'), 1)[0]

            return JsonResponse({
                'title': photo['caption'],
                'thumb': photo['thumb'],
                'url': photo['full'],
            })

        except:

            return HttpResponse(status=404)

