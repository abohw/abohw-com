from django.contrib import admin
from .models import Checkin, flickrCache

# Register your models here.

admin.site.register(Checkin)
admin.site.register(flickrCache)
