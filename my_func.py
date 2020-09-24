from telebot import types
from telebot.types import InlineKeyboardMarkup

from bd_config import Theme


def themekey(my_bot,user_id):
    theme_add_key = InlineKeyboardMarkup()
    theme_add_key.row(types.InlineKeyboardButton(text='➕ Добавить новую тему', callback_data='theme_add'))
    my_bot.send_message(user_id, 'Добавить новую тему?', reply_markup=theme_add_key)
    for theme in Theme.select():
        theme_key = InlineKeyboardMarkup()
        theme_key.row(types.InlineKeyboardButton(
            text='Редактировать', callback_data=f'red_{theme.id}'),
            types.InlineKeyboardButton(text='Удалить', callback_data=f'del_{theme.id}')
        )
        my_bot.send_message(user_id, f'📖{theme.name}', reply_markup=theme_key)



