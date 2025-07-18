from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField('Короткое описание')
    description_long = models.TextField('Длинное описание')
    lat = models.FloatField('Широта', blank=True, null=True)
    lon = models.FloatField('Долгота', blank=True, null=True)
    
    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Изображение')
    position = models.PositiveIntegerField('Позиция', default=0)
    
    def __str__(self):
        return f'{self.position} {self.place.title}'
