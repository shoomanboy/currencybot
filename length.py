import math
from geopy.distance import geodesic


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


if __name__ == "__main__":
    length(latitude, longitude, latitude1, longitude1)
