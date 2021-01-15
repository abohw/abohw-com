from django.core.management import BaseCommand
from django.conf import settings
from django.core.cache import cache

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

            if p['ispublic'] == 1 or p['isfriend'] == 1:

                results.append({
                    'thumb': 'https://farm%s.staticflickr.com/%s/%s_%s_c.jpg' % (p['farm'], p['server'], p['id'], p['secret']),
                    'full': 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % (p['farm'], p['server'], p['id'], p['secret']),
                    'caption': p['title'],
                    'sfw': (p['safety_level'] == '0'),
                })

        return results

    def handle(self, *args, **options):

        albums = me.getPhotosets()
        for album in albums:
            if album['id'] == '72157717269347353':
                cache.set('flickr_people', self.prepPhotos(album.getPhotos()), None)
            if album['id'] == '72157717269334156':
                cache.set('flickr_places', self.prepPhotos(album.getPhotos()), None)

        cache.set('flickr_latest', self.prepPhotos(me.getPublicPhotos())[:50], None)

        print("flickr cache updated successfully")
