from django.shortcuts import render
from django.db.models import Count
from django.core.cache import cache
from .models import Checkin, flickrCache

import random
import datetime


def error404(request, exception):
    return render(request, 'error404.html')


def webHome(request):

    numcountries = Checkin.objects.values('country').annotate(cc=Count('country')).count()
    numstates = Checkin.objects.filter(country='United States').values('state').annotate(cc=Count('state')).count()
    numcoffee_shops = Checkin.objects.filter(date__range=[datetime.date.today() - datetime.timedelta(days=365), datetime.date.today()]).filter(category__exact='Coffee Shops').values('venueid').distinct().count()
    numplaces = Checkin.objects.filter(date__range=[datetime.date.today() - datetime.timedelta(days=365), datetime.date.today()]).values('venueid').distinct().count()
    numphotos = flickrCache.objects.latest('id').numPastYear

    photos = cache.get('flickr_faves')

    response = render(request, 'index.html', {
        'numCountries': numcountries,
        'numStates': numstates,
        'numCoffeeShops': numcoffee_shops,
        'numPlaces' : numplaces,
        'numPhotos' : numphotos,
        'photos' : random.sample(photos, len(photos))[:4],
        })

    return response
