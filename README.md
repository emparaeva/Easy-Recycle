# "Easy Recycle" Telegram Bot

https://t.me/CleanSanBot

![video_2021-10-28_09-47-35 (online-video-cutter com)](https://user-images.githubusercontent.com/88197584/139203581-8459bed5-8be6-47a2-ac12-d8cc23ae9fac.gif)

## Задача

Реализовать сервис по грамотной и быстрой сортировке отходов для их утилизации и дальнейшей переработке

## План решения задачи

1) **Формирование датасета классов отходов и пунктов раздельного сбора мусора**
2) **Разметка фотографий и их аугментация**
3) **Выбор модели и её обучение на нейронных сетях**
4) **Создание сервиса**

## Решение задачи

### Формирование датасета классов отходов и пунктов раздельного сбора мусора
Были определены 6 классов отходов (пластик, бумага, металл, органические материалы природного происхождения, стекло, композитные материалы) и сделан датасет из 1400 фотографий. Также вручную был сделан датасет из пунктов раздельного сбора мусора по г.Москве для выбранных классов (около 400 точек).
### Разметка фотографий и их аугментация
Разметка фотографий была осуществлена с помощью сервиса [Make Sense](https://www.makesense.ai/). С помощью [Roboflow](https://roboflow.com/) была проведена аугментация фотографий. В конечном итоге количество фотографий выросло до 5000. Полученные данные были разделены на train, valid и test.
### Выбор модели и её обучение на нейронных сетях
В качестве моделей были выбраны нейронные сети darknet YOLOv4, и с помощью Google Colab Pro они были обучены на видеокарте GPU Type: Tesla P100-PCIE-16GB. Метрикой в моделях Yolov4 DarkNet служила Mean Average Precision.
- Первая модель детектирует один из шести видов отходов по фотографии. Обучение заняло около 15 часов. Оценка точности на валидационной выборке 72%.
- Вторая модель определяет, является ли пластик перерабатываемым. Обучение заняло около 10 часов. Оценка точности на валидационной выборке 71%.
### Создание сервиса
В качестве сервиса был выбран Telegram Бот [@CleanSanBot](https://t.me/CleanSanBot). При создании бота была использована библиотека Аiogram, которая помогла реализовать State запросы, запросы пользователя, клавиатуры ReplyKeyboardMarkup и InlineKeyboardMarkup и отправку сообщениий пользователю.
## Принцип работы сервиса:
- Пользователь запускает telegram бот и присылает фотографию со значком переработки отходов:
![IMG_20211019_171421_1](https://user-images.githubusercontent.com/88563421/139556482-769861c5-6133-4c48-9589-b42b601fcded.jpg)
- Фотография поступает на проверку отправленного сообщения (проверяется, что на вход пришла фотография, а не текст)
- Пользователю предлагается разрешить использовать его местоположение
- Если пользователь даёт согласие:
  - Eго координаты записываются в датасет (все данные конфиденциальные)
  - Далее фотография поступает на вход первой модели darknet YOLOv4 и определяется тип отходов на фотографии
  - Если классов несколько, то пользователю предлагается выбрать, какой класс отходов он хочет правильно утилизировать
  - Если выбранный класс является пластиком, то фотография поступает на вторую модель darknet YOLOv4, которая детектирует, является ли пластик перерабатываемым
  - С помощью координат пользователя и координат местоположения пунктов раздельного сбора мусора высчитываются три ближайших адреса, куда можно сдать данный тип мусора и выводятся пользователю в виде сообщения
  - Если обнаружен только один класс, то пользователю сразу выводится в виде сообщения три ближайших адреса подходящих пунктов раздельного сбора мусора
- Если пользователь отказался:
  - Его фотография поступает на вход модели darknet YOLOv4 и определяется тип отходов, присутствующих на фотографии
  - Если среди обнаруженных классов есть пластик, то фотография поступает на вторую модель Yolov4 DarkNet, которая определяет, является ли пластик перерабатываемым
  - Выводится сайт, где пользователь может посмотреть все точки на карте, где можно сдать мусор
## Способ проверки работоспособности кода:
1) Установить все библиотеки из requirements.txt (for windows - pip install - r requirements.txt)
2) В bot/api/ создать папку database
3) В [Google drive](https://drive.google.com/drive/folders/1_K7dKHxCFKUMlBCmlu7Rq7LuF9AnW5LM?usp=sharing) скачать датасет и поместить в database. Веса поместить в папку bot/api/core/darknet-master/
4) По примеру файла .env.dist создать в корневой папке файл .env с TOKEN_TELEGRAM и ключевыми словами с кодами
5) Запустить скрипт bot/_bot.py
## Авторы:
1) https://github.com/emparaeva
2) https://github.com/Deibrony
3) https://github.com/RyzhkovIlya
