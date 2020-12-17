import math
from geopy.distance import geodesic
import googlemaps
gmaps = googlemaps.Client(key='KEY')


def length(latitude, longitude, latitude1, longitude1):
    """применение формулы"""
    # R = 6373  # Radius of the earth
    # dlat = abs(latitude - latitude1)  # change in coordinates
    # dlon = abs(longitude - longitude1)
    # a = math.sin(dlat / 2) ** 2 + math.cos(latitude) * math.cos(latitude1) * math.sin(
    #     dlon / 2) ** 2  # haversine formula
    # c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # distance = R * c*1.6
    # # print(round(distance,1))
    """Применение geopy"""
    selflocation = (latitude, longitude)
    location = (latitude1, longitude1)
    distance = geodesic(selflocation, location).kilometers
    return round(distance, 2)


def length_top5(latitude, longitude,latitude1, longitude1):
    selflocation = "%s %s"%(latitude, longitude)
    location = "%s %s"%(latitude1, longitude1)
    range = gmaps.distance_matrix(selflocation, location)['rows'][0]['elements'][0]
    distance=float(range["distance"]["text"].replace("km",""))
    return distance



