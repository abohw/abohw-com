from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache

import random


def photosHome(request, page=''):

    try:
        photos = getCollection(page)

    except:
        photos = None

    return render(request, 'photos/index.html', { 'photos' : photos })


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
