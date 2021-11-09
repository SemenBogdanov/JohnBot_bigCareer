"""
This is a echo bot.
It echoes any incoming text messages.git
"""

import logging
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from key import token
from aiogram import Bot, Dispatcher, executor, types
from answers import answers, answers2
import keyboards

API_TOKEN = token
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
call_data1 = CallbackData('data', 'num')
call_data2 = CallbackData('wantAsk', 'wantAsk')


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("""Добрый день!\n"""
                        """Выбирайте самый сложный путь - там не конкурентов!\n\n"""
                        """Ниже есть кнопка, чтоб увидеть ответы на часто задаваемые вопросы. """,
                        reply_markup=keyboards.keyboard2())


def get_keyboard():
    return InlineKeyboardMarkup().row(
        KeyboardButton('Пора ли звонить?', callback_data=call_data1.new(num='1')),
    ).row(
        KeyboardButton('Услуги и цены', callback_data=call_data1.new(num='2')),
        KeyboardButton('Алгоритм работы', callback_data=call_data1.new(num='3')),
    ).row(
        KeyboardButton('Команда', callback_data=call_data1.new(num='4')),
        KeyboardButton('Контакты', callback_data=call_data1.new(num='5')),
        KeyboardButton('Об авторе...', callback_data=call_data1.new(num='6')),
    ).row(
        InlineKeyboardButton(text='Оставить заявку и получить бонус!', url='https://big-career.ru/',
                             callback_data=call_data1.new(num='7')),)


def keyboard2():
    return ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton('---Задать вопрос!---'))


@dp.message_handler(text=['---Задать вопрос!---'])
async def ask(message: types.Message):
    await message.reply('Выберите вопрос и нажмите кнопку:\n', reply_markup=get_keyboard())


@dp.callback_query_handler(keyboards.call_data1.filter(num1=['1', '2', '3', '4', '5', '6', '7']))
async def callback_reply(query: types.CallbackQuery, callback_data):
    await query.answer()
    if callback_data['num1'] == '2':
        await bot.send_message(query.from_user.id, 'Выберите вариант:',
                               reply_markup=keyboards.keyboard3())
    else:
        ans = answers[int(callback_data['num1']) - 1]
        await bot.send_message(query.from_user.id, ans, parse_mode='html')
    # logging.info('This what we have got %r', callback_data)
    # logging.info('This is calldata1 %r', call_data1)


@dp.callback_query_handler(keyboards.call_data3.filter(num2=['0', '1', '2', '3']))
async def callback_reply(query: types.CallbackQuery, callback_data):
    await query.answer()
    ans = answers2[int(callback_data['num2'])]
    await bot.send_message(query.from_user.id, ans, parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
