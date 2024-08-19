from math import radians, sin, cos, sqrt, atan2
 
import reverse_geocoder as rg

def distance_geo(lat1, lon1, lat2, lon2):
    R = 6371.0
    
    # Конвертация градусов в радианы
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    # Разница координат
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    # Формула хаверсинуса
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    
    return distance

def reverseGeocode(coordinates): #обратное геокодирование
    result = rg.search(coordinates)
    return result[0]['name']