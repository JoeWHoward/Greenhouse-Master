from django.db import models

# Create your models here.
class TempHumRecord(models.Model):
    date_time_logged = models.DateTimeField(auto_now_add=True)
    temp = models.FloatField(blank=True)
    humidity = models.FloatField(blank=True)

    class Meta:
        verbose_name = "Temperature Record"