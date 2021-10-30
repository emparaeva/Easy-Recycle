import os
import os.path
import logging
import time
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from api.main import recommender_address, plastic_recommend
from api.static import START, INFO, NEW_PLASTIC, ADDRESS, CLASS_TRASH_1, CLASS_TRASH__ALL, \
NOT_CLASS, NOT_LOC, TRY_AGAIN, STICKER, LOC_AWARNES, LOW_BUTTON, CLASS_TYPE
from api.core.location_dict import location_add
from api.core.result import result_out
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Загрузка токена через env
load_dotenv()
TOKEN = os.getenv('TOKEN_TELEGRAM')
YES = os.getenv('YES')
NO = os.getenv('NO')
PLASTIC = os.getenv('PLASTIC')
PAPER = os.getenv('PAPER')
METAL = os.getenv('METAL')
ORGAN = os.getenv('ORGAN')
GLASS = os.getenv('GLASS')
COMPOS = os.getenv('COMPOS')
ALL = os.getenv('ALL')


markup = ReplyKeyboardMarkup(resize_keyboard=True)
location_button = KeyboardButton('Прислать геолокацию', request_location=True)
markup.add(location_button)

inline_btn_1 = InlineKeyboardButton('Да', callback_data=YES)
inline_btn_2 = InlineKeyboardButton('Нет', callback_data=NO)
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1).add(inline_btn_2)

inline_plastic = InlineKeyboardButton('Пластик', callback_data=PLASTIC)
inline_paper = InlineKeyboardButton('Бумага', callback_data=PAPER)
inline_metal = InlineKeyboardButton('Металл', callback_data=METAL)
inline_oganic = InlineKeyboardButton('Органические материалы', callback_data=ORGAN)
inline_glass = InlineKeyboardButton('Стекло', callback_data=GLASS)
inline_composite = InlineKeyboardButton('Композитные материалы', callback_data=COMPOS)
inline_all = InlineKeyboardButton('Все сразу', callback_data=ALL)

# Логирование
logging.basicConfig(filename='log.log',
                    level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logging.info(f'{user_id} запустил бота в {time.asctime()}')
    await message.answer(START % user_name)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(INFO)

@dp.message_handler(content_types=['location'])
async def handle_loc(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    mess = message.location
    current_position = (mess.longitude, mess.latitude)
    coords = [current_position[0], current_position[1]]
    location_add(coords, user_id, user_name)

@dp.callback_query_handler(lambda c: c.data in [YES, NO], state='*')
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id

    if callback_query.data == YES:
        await bot.send_sticker(user_id, STICKER) # Отправка пользователю сообщения, пока предсказывает модель
        await callback_query.message.answer(LOW_BUTTON, reply_markup=markup)
        class_list = result_out() # Результат предсказания
        await state.update_data(my_classes=class_list)
        if class_list == TRY_AGAIN:
            await bot.send_message(user_id, TRY_AGAIN)
        else:
            if len(set(class_list)) == 1:
                await bot.send_message(user_id, CLASS_TRASH_1 + '🚯'+'\n'.join(set(class_list))) # Отправка пользователю сообщения с определенным классом
                await bot.send_message(user_id, ADDRESS + recommender_address(class_list), parse_mode = "Markdown") # Отправка пользователю 3х адрессов пунктов приема данного типа отходов

    if callback_query.data == NO:
        await bot.send_sticker(user_id, STICKER) # Отправка пользователю сообщения, пока предсказывает модель
        class_list = result_out() # Результат предсказания
        if class_list == TRY_AGAIN:
            await bot.send_message(user_id, TRY_AGAIN)
        else:
            if len(set(class_list)) == 1:
                await bot.send_message(user_id, CLASS_TRASH_1 + '🚯'+'\n'.join(set(class_list))) # Отправка пользователю сообщения с определенным классом
                plastic_class = plastic_recommend(set(class_list))
                if plastic_class == 'good':
                    await bot.send_message(user_id, NOT_LOC)
                else:
                    await bot.send_message(user_id, plastic_class)
            else:
                await bot.send_message(user_id, CLASS_TRASH__ALL + '🚯'+'\n🚯'.join(set(class_list))) # Отправка пользователю сообщения с определенным классом
                plastic_class = plastic_recommend(set(class_list))
                if plastic_class == 'good':
                    await bot.send_message(user_id, NOT_LOC)
                else:
                    await bot.send_message(user_id, plastic_class + NEW_PLASTIC)

    if len(set(class_list)) > 1 and callback_query.data != NO:
        inline_class = InlineKeyboardMarkup()
        set_classes = set(class_list)
        class_type = {'1-9 Plastic':inline_plastic, '20-23 Paper':inline_paper, '40-41 Metal':inline_metal, '50-61 Organic materialc':inline_oganic, '70-79 Glass':inline_glass, '80-97 Composite materials':inline_composite}
        for cl in set_classes:
            inline_class.add(class_type[cl])
        inline_class.add(inline_all)
        await callback_query.message.answer(CLASS_TYPE, reply_markup=inline_class)

@dp.callback_query_handler(lambda c: c.data in [PLASTIC, PAPER, METAL, ORGAN, GLASS, COMPOS, ALL], state='*')
async def process_callback_button2(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    async with state.proxy() as data:
        user_calss = data['my_classes']
    result_type = {PLASTIC:'1-9 Plastic', PAPER:'20-23 Paper', METAL:'40-41 Metal', ORGAN:'50-61 Organic materialc', GLASS:'70-79 Glass', COMPOS:'80-97 Composite materials', ALL:set(user_calss)}
    await bot.send_message(user_id, ADDRESS + recommender_address([result_type[callback_query.data]]), parse_mode = "Markdown") # Отправка пользователю 3х адрессов пунктов приема пластика

@dp.message_handler(content_types=['photo'])
async def echo_message(message: types.Message):
    photo = message.photo
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    if message.content_type != 'photo' :
        await bot.send_message(user_id, NOT_CLASS)
    else:
        logging.info(f'Нам написал {user_name}, его id = {user_id}')
        await photo[-1].download('data/' + 'prediction' + '.jpg') #сохранение фотографии, отправленой пользователем
        await message.answer(LOC_AWARNES, reply_markup=inline_kb1)
        
if __name__ == '__main__':
    executor.start_polling(dp)