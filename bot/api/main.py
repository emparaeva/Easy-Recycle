import logging
from api.core.distnce import distance
from api.core.plastic import pred_plastic
from api.static import BAD_PLASTIC, NOT_LOC
logging.basicConfig(filename='log.log',level=logging.INFO) 

def recommender_address(classes):
    '''Функция принимает на вход список найденных классов и возвращает 3 самых ближайших адреса пункта приема отходов'''

    if '1-9 Plastic' in classes:
        if pred_plastic() == 'Good':
            return distance(classes)
        else:
            return BAD_PLASTIC
    else:
        return distance(classes)

def plastic_recommend (classes):
    '''Функция принимает на вход список найденных классов, где имеется пластик и возвращает метку, можно его перерабатываь или нет'''

    if '1-9 Plastic' in classes:
        if pred_plastic() == 'Good':
            return('good')
        else:
            return(BAD_PLASTIC)
    else:
        return 'good'