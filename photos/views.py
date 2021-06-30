from django.shortcuts import render
from django.conf import settings
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

    if request.COOKIES.get('contra') or request.user.is_authenticated:
        photos = cache.get('flickr_random')

    else:
        photos = cache.get('flickr_faves')

    photos = random.sample(photos, 4)

    return render(request, 'photos/random.html', { 'photos' : photos, })