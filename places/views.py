from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .models import Place, Image
from django.db.models import Prefetch


def index(request):
    places = Place.objects.all()
    features = []

    for place in places:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.place_id,
                "detailsUrl": reverse('place-json', args=[place.place_id])
            }
        })

    places_geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    context = {
        'places_geojson': places_geojson
    }
    return render(request, 'index.html', context)


def places_json(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related('images'),
        place_id=place_id
    )

    images = place.images.all()

    image_urls = [image.image.url for image in images]

    place_properties = {
        "title": place.title,
        "imgs": image_urls,
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {
            "lng": place.lng,
            "lat": place.lat
        }
    }

    return JsonResponse(place_properties, json_dumps_params={'ensure_ascii': False, 'indent': 4})
