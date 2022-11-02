from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

inline_markup = InlineKeyboardBuilder()
inline_markup.button(text='Да', callback_data='Да')
inline_markup.button(text='Нет', callback_data='Нет')
