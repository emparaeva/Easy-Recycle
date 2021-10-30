import pandas as pd
from api.core.function_dist import func_dist
from api.core.classificate import new_class

def distance(trash_class):
    '''Функция принимает на вход класс отхода и возвращает адрес топ-3 ближайших пунктов сбора данного класса мусора'''

    new_trash_class = new_class(trash_class) # С помощью функции new_class получает список из новых классов
    df = pd.read_excel('bot/api/database/garbage_points_msc.xlsx') # открываем датасет со списками всех пунктов сбора отходов
    df.Class = df.Class.apply(lambda x: eval(x)) # Каждый элемент признака Class переводим в питоновский формат
    df['Coordinates'] = df['Coordinates'].apply(lambda x: eval(x)) # Каждый элемент признака Coordinates переводим в питоновский формат
    if len(new_trash_class) > 1: # Проверяем,что длина списка с новыми классами была больше 1
        df_class = df[df['Class'].apply(lambda x: any([i in x for i in new_trash_class]))] # Оставляем только те записи в датасете, где в признакке Class присутствует любой класс из списка новых классов
    else:
        df_class = df[df['Class'].apply(lambda x: new_trash_class[0] in x)] # Оставляем только те записи в датасете, где в признакке Class присутствует найденный класс из списка нового класса
    df_class['dist_point'] = df_class['Coordinates'].apply(lambda x: func_dist(x)) # Создаем новый признак, куда заносим найденные расстояния от пользователя, до пунктов приема отходов
    return '♻️'+'\n♻️'.join(df_class.sort_values('dist_point', ascending = True).head(3)['Address'].to_list()) # Возвращаем 3 ближайших пункта сбора отходов