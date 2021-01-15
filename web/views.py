from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.db.models import Count
from .models import Checkin

import datetime


def error404(request, exception):
    return render(request, 'error404.html')


def webHome(request):

    t = get_template('index.html')

    countries = Checkin.objects.values('country').order_by('country').annotate(cc=Count('country')).count()
    states = Checkin.objects.filter(country='United States').values('state').order_by('state').annotate(cc=Count('state')).count()

    html = t.render({
    'countries': countries,
    'states': states,
    })

    return HttpResponse(html)
