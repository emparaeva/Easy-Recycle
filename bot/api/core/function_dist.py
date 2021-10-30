from api.core.km import km
import pandas as pd
def func_dist(point_loc):
    '''Функция принимает на вход координаты пункта сбора отходов и возвращает расстояние от пользователя, то пункта'''

    df = pd.read_csv('bot/api/database/users_location.csv') # Открываем датасет с данными пользователя
    gps = eval(df.loc[len(df)-1].location) # Берем последнюю запись в признаке location
    lat_1 = point_loc[0] 
    lng_1 = point_loc[1]
    lat_2 = gps[1]
    lng_2 = gps[0]
    road = km(float(lat_1), float(lng_1), float(lat_2), float(lng_2)) # Вычисляем расстояние от пользователя до ближайших пунктов приема отходов с помощью функции km
    return road