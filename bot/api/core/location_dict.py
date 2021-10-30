import pandas as pd
import os.path
from datetime import datetime

def location_add(loc, id_user, user_name):
    '''Функция принимает на вход местоположение пользователя и его ID и записывает это парой ключ-значение в словарь.'''
    
    if not os.path.exists('bot/api/database/users_location.csv'):
        df = pd.DataFrame(columns=['user_name','id', 'location', 'datetime'])
        df.loc[len(df)] = [user_name, id_user, loc, datetime.now()]
        df.to_csv('bot/api/database/users_location.csv', index=False)
    else:
        df = pd.read_csv('bot/api/database/users_location.csv')
        df.loc[len(df)] = [user_name, id_user, loc, datetime.now()]
        df.to_csv('bot/api/database/users_location.csv', index=False)