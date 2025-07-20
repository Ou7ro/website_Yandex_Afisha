from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Place


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
            "detailsUrl": "static/places/moscow_legends.json"
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
    place = get_object_or_404(Place, place_id=place_id)
    
    images = place.images.order_by('position')
    
    image_urls = [image.image.url for image in images]
    
    place_properties = {
		"title": place.title,
    	"imgs": image_urls,
    	"description_short": place.description_short,
    	"description_long": place.description_long,
    	"coordinates": {
    		"lng": place.lng,
    	    "lat": place.lat
    	}
  	} 	
    
    return JsonResponse(place_properties, json_dumps_params={'ensure_ascii': False, 'indent': 4})
    
