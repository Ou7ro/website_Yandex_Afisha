from django.core.management.base import BaseCommand, CommandError
import requests
from places.models import Place, Image
from requests.exceptions import RequestException
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Load places from JSON URL into database'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_url',
            type=str,
            help='Full URL to JSON file with place data'
        )

    def handle(self, *args, **options):
        json_url = options['json_url']
        try:
            response = requests.get(json_url, timeout=10)
            response.raise_for_status()
            place_property = response.json()
        except RequestException as e:
            raise CommandError(f'Ошибка загрузки JSON: {str(e)}')
        except ValueError:
            raise CommandError('Некорректный формат JSON')

        try:
            place, created = self.create_place(place_property)
            if created:
                try:
                    self.load_images(place, place_property['imgs'])
                except RequestException as e:
                    raise CommandError(f'Ошибка загрузки изображений: {str(e)}')
        except (KeyError, ValueError) as e:
            raise CommandError(f'Ошибка сохранения места: {str(e)}')

    def create_place(self, property):
        return Place.objects.get_or_create(
            title=property['title'],
            defaults={
                'title': property['title'],
                'description_short': property.get('description_short', ''),
                'description_long': property.get('description_long', ''),
                'lng': float(property['coordinates']['lng']),
                'lat': float(property['coordinates']['lat']),
            }
        )

    def load_images(self, place, image_urls):
        for position, image_url in enumerate(image_urls, start=1):
            response = requests.get(image_url)
            response.raise_for_status()

            img_name = self.extract_filename(image_url)
            img_content = ContentFile(
                response.content,
                name=img_name
            )

            Image.objects.create(
                place=place,
                image=img_content,
                position=position
            )

    def extract_filename(self, url):
        return url.split('/')[-1].split('?')[0]
