from django.core.management.base import BaseCommand, CommandError
import requests
from places.models import Place, Image
from io import BytesIO
from django.core.files import File
from requests.exceptions import MissingSchema, RequestException


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
            place, _ = self.create_place(place_property)
        except (KeyError, ValueError) as e:
            raise CommandError(f'Ошибка сохранения места: {str(e)}')

        try:
            self.load_images(place, place_property['imgs'])
        except RequestException as e:
            raise CommandError(f'Ошибка загрузки изображений: {str(e)}')

    def create_place(self, property):
        return Place.objects.get_or_create(
            place_id=property.get('place_id', self.generate_place_id(property['title'])),
            defaults={
                'title': property['title'],
                'description_short': property.get('description_short', ''),
                'description_long': property.get('description_long', ''),
                'lng': float(property['coordinates']['lng']),
                'lat': float(property['coordinates']['lat']),
            }
        )

    def load_images(self, place, image_urls):
        for image_url in image_urls:
            response = requests.get(image_url)
            response.raise_for_status()
            img_file = BytesIO(response.content)
            img_name = self.extract_filename(image_url)
            image = Image(place=place)
            image.image.save(img_name, File(img_file))
            image.save()

    def extract_filename(self, url):
        return url.split('/')[-1].split('?')[0]

    def generate_place_id(self, title):
        return title.lower().replace(' ', '-')
