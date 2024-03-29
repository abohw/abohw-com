from django.core.management import BaseCommand
from django.conf import settings
from django.core.cache import cache
from web.models import flickrCache
from django.utils import timezone

import pytz
import random
import datetime
import flickr_api
from flickr_api.auth import AuthHandler

handler = AuthHandler(
    key = settings.FLICKR_KEY, secret = settings.FLICKR_SECRET,
    access_token_key = settings.FLICKR_AUTH_KEY, access_token_secret = settings.FLICKR_AUTH_SECRET)
flickr_api.set_auth_handler(handler)
me = flickr_api.test.login()

class Command(BaseCommand):

    help = "fill the cache with flickr data"

    def prepPhotos(self, photos):

        results = []

        for photo in photos:
            p = flickr_api.Photo.getInfo(photo)

            if p['media'] != 'video':

                if p['ispublic'] == 1 or p['isfriend'] == 1:

                    results.append({
                        'thumb': 'https://farm%s.staticflickr.com/%s/%s_%s_c.jpg' % (p['farm'], p['server'], p['id'], p['secret']),
                        'full': 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % (p['farm'], p['server'], p['id'], p['secret']),
                        'caption': p['title'],
                        'safety': p['safety_level'],
                    })

        return results

    def handle(self, *args, **options):

        albums = me.getPhotosets()
        for album in albums:
            if album['id'] == '72157717269347353':
                cache.set('flickr_people', self.prepPhotos(album.getPhotos(safe_search='2')), None)
            if album['id'] == '72157717269334156':
                cache.set('flickr_places', self.prepPhotos(album.getPhotos(safe_search='2')), None)
            if album['id'] == '72157718184167491':
                cache.set('flickr_faves', self.prepPhotos(random.sample(album.getPhotos(safe_search='1', per_page='500'), 50)), None)

        cache.set('flickr_latest', self.prepPhotos(me.getPublicPhotos(safe_search='1', per_page='30')), None)
        cache.set('flickr_random', self.prepPhotos(random.sample(me.getPhotos(safe_search='2', per_page='500'), 50)), None)

        numPastYear = me.getPhotoCounts(
            taken_dates='%s,%s' % (
                datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=365), '%Y-%m-%d'),
                datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d'))
        )[0]['count']

        numTotal = me.getPhotos().info.total

        flickrCache.objects.create(
            numPastYear = numPastYear,
            numTotal = numTotal,
        )

        flickrCache.objects.filter(lastUpdated__lt=(timezone.now() - datetime.timedelta(days=7))).delete()

        print('flickr cache updated, %s photos in total' % (numTotal))
