from international.models import countries
from django.db import models
from flight.models import Flight



class Booking(models.Model):
    user = models.ForeignKey('auth.User', blank=True, null=True)
    flight_id = models.ForeignKey(Flight, verbose_name='Flight')
    street1 = models.CharField(verbose_name='Street 1',
                               max_length=256, blank=True)
    street2 = models.CharField(verbose_name='Street 2',
                               max_length=256, blank=True)
    city = models.CharField(verbose_name='City',
                            max_length=256, blank=True)
    zipcode = models.CharField(verbose_name='Zip/Postal Code',
                               max_length=256, blank=True)
    country = models.CharField(verbose_name='Country', max_length=2,
                               choices=countries, blank=True)
    taken_seats = models.IntegerField()
    created_at = models.DateTimeField(verbose_name='Created At',
                                         auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return '#{} ({})'.format(self.pk, self.created_at)
