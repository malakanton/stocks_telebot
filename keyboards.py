from aiogram.types import InlineKeyboardMarkup, \
                          InlineKeyboardButton, \
                          ReplyKeyboardMarkup, \
                          KeyboardButton

def chart_kb(url: str):
    ikb = InlineKeyboardMarkup(row_width=1)

    ikb.add(
        InlineKeyboardButton(text='Chart Link',
                             url=url)
    )
    return ikb


def help_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True,
                             one_time_keyboard=True)
    kb.add(
        KeyboardButton('/help'),
        KeyboardButton('/start'),
        KeyboardButton('/description')
        )
    return kb


def actions_cb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton('/about ℹ️'),
        KeyboardButton('/chart 📈'),
        KeyboardButton('/analytics 📄'),
        KeyboardButton('/sustainability 🌎'),
        KeyboardButton('/dividend 💵')
        )
    return kb
