from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache

import random

def photosHome(request, page=''):

    try:
        photos = getCollection(page, (request.GET.get('s') == 'd'))

    except:
        photos = None

    return render(request, 'photos/index.html', {
            'photos' : photos,
            'page' : page, })

def getCollection(page, nsfw):

    display = 30

    if page == 'people':
        photos = cache.get('flickr_people')

    elif page == 'places':
        photos = cache.get('flickr_places')

    else:
        photos = cache.get('flickr_latest')
        display = 15

    if nsfw is False:
        collection = []

        for photo in photos:
            if photo['sfw'] is True:
                collection.append(photo)

    else: collection = photos

    collection = collection[:display]
    return random.sample(collection, len(collection))
