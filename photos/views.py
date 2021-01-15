from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from django.core.cache import cache

import random

def photosHome(request, page=''):

    t = get_template('photos/index.html')

    try:
        photos = getCollection(page, (request.GET.get('s') == 'd'))

    except:
        photos = None

    html = t.render({
        'photos' : photos,
        'page' : page, })

    return HttpResponse(html)

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
