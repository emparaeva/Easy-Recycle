def new_class(res):
    '''Функция принимает на вход список класса отходов и возвращает категориальные классы.'''

    class_dict = {'1-9 Plastic':0, '20-23 Paper':1, '40-41 Metal':2, '50-61 Organic materialc':3, '70-79 Glass':4, '80-97 Composite materials':5} #словарь классов
    pred = [] # Пустой список
    if len(res[0]) > 6: # Проверка на длину первого элемента входного списка
        if len(set(res)) == 1: # Проверка на длину входного списка
            pred.append(class_dict[res[0]]) # Добавление нового класса в список pred
    else:
        for i in res[0]: # Проход циклом по каждому элементу из входного списка
            pred.append(class_dict[i]) # Добавление нового класса в список pred
    return pred