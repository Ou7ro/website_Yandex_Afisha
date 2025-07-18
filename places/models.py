from django.db import models

class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    #imgs = models.ForeignKey()
    description_short = models.TextField('Короткое описание')
    description_long = models.TextField('Длинное описание')
    lat = models.FloatField('Широта', blank=True, null=True)
    lon = models.FloatField('Долгота', blank=True, null=True)
    
    def __str__(self):
        return self.title