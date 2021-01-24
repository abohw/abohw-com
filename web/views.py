from django.shortcuts import render
from django.db.models import Count
from .models import Checkin, flickrCache

import datetime


def error404(request, exception):
    return render(request, 'error404.html')


def webHome(request):

    countries = Checkin.objects.values('country').annotate(cc=Count('country')).count()
    states = Checkin.objects.filter(country='United States').values('state').annotate(cc=Count('state')).count()
    coffee_shops = Checkin.objects.filter(date__range=[datetime.date.today() - datetime.timedelta(days=365), datetime.date.today()]).filter(category__exact='Coffee Shops').values('venueid').distinct().count()
    places = Checkin.objects.filter(date__range=[datetime.date.today() - datetime.timedelta(days=365), datetime.date.today()]).values('venueid').distinct().count()
    photos = flickrCache.objects.latest().numPastYear

    return render(request, 'index.html', {
        'numCountries': countries,
        'numStates': states,
        'numCoffeeShops': coffee_shops,
        'numPlaces' : places,
        'numPhotos' : photos,
        })
