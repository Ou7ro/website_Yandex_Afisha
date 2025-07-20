from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    place_id = models.CharField('Id места', null=True, blank=True)
    description_short = models.TextField('Короткое описание')
    description_long = models.TextField('Длинное описание')
    lng = models.FloatField('Долгота', null=True, blank=True)
    lat = models.FloatField('Широта', null=True, blank=True)
    
    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Изображение')
    position = models.PositiveIntegerField('Позиция', default=0)
    
    def __str__(self):
        return f'{self.position} {self.place.title}'
