from geopy.geocoders import Nominatim
geolocator = Nominatim()


def geocode(address):
    return geolocator.geocode(address)
