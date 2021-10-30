from api.static import PH
import os
from api.static import TRY_AGAIN

def result_out():
    '''Функция принимает возвращает список классов, которые были обнаружены на фотографии.'''

    os.system(f'{PH}darknet.exe detector test {PH}cfg/coco.data {PH}cfg/custom-yolov4-detector.cfg {PH}72custom-yolov4-detector_best.weights C:/Easy_Recycle/data/prediction.jpg -thresh 0.8 -dont-show -ext_output < {PH}data/train.txt > {PH}result.txt')
    with open(f'{PH}result.txt') as f:
        text = f.read()
        text = text.split('\n')
        text = list(filter(None, text))
        if len(text) > 12:
            text_1 = text[12:]
            all_results = [i.split(':')[0] for i in text_1]
            return all_results
        else:
            return(TRY_AGAIN)
    
def result_out_plastic():
    '''Функция принимает возвращает список классов, которые были обнаружены на фотографии пластика.'''

    with open(f'{PH}result_plastic.txt') as f:
        text = f.read()
        text = text.split('\n')
        text = list(filter(None, text))
        if len(text) > 7:
            text_2 = text[7:]
            plastic_results = [i.split(':')[0] for i in text_2]
            return plastic_results