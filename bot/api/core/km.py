from math import *
from geopy.distance import geodesic

def km (lat_1, lng_1, lat_2, lng_2):
    '''Функция рассчитывает расстояние между двумя точками'''

    return(geodesic((lat_1,lng_1), (lat_2,lng_2)). m) # Вычисляем расстояние от пользователя до ближайших пунктов приема отходов с помощью библиотеки geodesic