from django.db import models
import slat.model_choices as mc

class SLATForm(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    byuid = models.CharField(max_length=9)
    language = models.CharField(max_length=100, choices= mc.slat.languages, default='')
    thesis = models.DateField()
    transcript = models.FileField()
    opi = models.FileField()