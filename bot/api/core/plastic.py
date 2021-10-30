from api.core.result import result_out_plastic
from api.static import BAD_PLASTIC
import os
from api.static import PH

def pred_plastic():
    '''Функция принимает на вход фотографию пластика и возвращает памятку, можно ли этот пластик перерабатывать.'''

    os.system(f'{PH}darknet.exe detector test {PH}cfg/2coco.data {PH}cfg/custom-yolov4-detector_plastic.cfg {PH}71_plastic_custom-yolov4-detector_best.weights C:/Easy_Recycle/data/prediction.jpg -thresh 0.6 -dont-show -ext_output < {PH}data/train_plastic.txt > {PH}result_plastic.txt')
    plastic_class = result_out_plastic()
    if 'Can-t be recycled' in plastic_class:
        return BAD_PLASTIC
    else:
        return ('Good')