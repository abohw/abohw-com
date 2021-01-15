from django.core.management import BaseCommand
from django.db.models import Count
from django.conf import settings
from web.models import Checkin

import foursquare
import datetime

class Command(BaseCommand):
    help = 'what'

    def add_arguments(self, parser):
        parser.add_argument('initial', type=str)

    def handle(self, *args, **options):

        fsq = foursquare.Foursquare(
            client_id=settings.FS_CLIENT_ID,
            client_secret=settings.FS_CLIENT_SECRET,
            access_token=settings.FS_ACCESS_TOKEN)

        if options['initial'] == 'initial':
            places = fsq.users.all_checkins()
        else:
            places = fsq.users.checkins()['checkins']['items']

        results = ''
        new = 0

        for item in places:
            try:

                if Checkin.objects.filter(fsqid__exact=item['id']).count() == 0:

                    for x in item['venue']['categories']:
                        try:
                            categoryid = 0

                            if x['primary'] is True:
                                category = x['pluralName']

                        except KeyError: pass
                        except IndexError: pass

                        checkin = Checkin(
                        fsqid=item['id'],
                        name=item['venue']['name'],
                        venueid=item['venue']['id'],
                        city=item['venue']['location']['city'],
                        state=item['venue']['location']['state'],
                        country=item['venue']['location']['country'],
                        date=datetime.datetime.fromtimestamp(item['createdAt']).strftime('%Y-%m-%d'),
                        category=category
                        )

                        checkin.save()

                        new =+ 1

            except KeyError:
                pass
            except IndexError:
                pass

        print('%s checkins added' % (new))
