from django.db import models

# Create your models here.

class flickrCache(models.Model):
    numTotal = models.IntegerField(default=0, db_index=True)
    numPastYear = models.IntegerField(default=0, db_index=True)
    lastUpdated = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-lastUpdated"]
        get_latest_by = ["-lastUpdated"]

    def __str__(self):
        return self.lastUpdated.strftime('%m/%d/%Y %H:%M')


class Checkin(models.Model):
    fsqid = models.CharField(max_length=24, primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    venueid = models.CharField(max_length=24, db_index=True)
    date = models.DateField(auto_now_add=True, db_index=True)
    category = models.CharField(max_length=50, db_index=True)
    city = models.CharField(max_length=25, db_index=True)
    state = models.CharField(max_length=25, db_index=True)
    country = models.CharField(max_length=25, db_index=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return '%s: %s' % (self.date.strftime('%m/%d/%Y'), self.name)
