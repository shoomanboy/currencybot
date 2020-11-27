import math




def length(latitude, longitude, latitude1, longitude1):
    R = 6373  # Radius of the earth
    dlat = abs(latitude - latitude1)  # change in coordinates
    dlon = abs(longitude - longitude1)
    a = math.sin(dlat / 2) ** 2 + math.cos(latitude) * math.cos(latitude1) * math.sin(
        dlon / 2) ** 2  # haversine formula
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    # print(round(distance,1))
    return distance


if __name__ == "__main__":
    length(latitude, longitude, latitude1, longitude1)
