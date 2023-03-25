from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
import bs
import search_company
from config import API_KEY
import bots_replies as br
import keyboards as k

MAX_LEN = 4096

with open('tickers_list.txt', 'r') as f:
    tickers_list = f.readline().split()

bot = Bot(API_KEY)
dp = Dispatcher(bot)

market_beat = None


def send_message(message: types.Message, text: str, kb=None):
    return message.answer(text=text, parse_mode='html', reply_markup=kb)


async def on_startup(_):
    print('Bot is active.')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    hello_msg = f'Hello, <b>{message.from_user.first_name}</b>!\n{br.DESCRIPTION}'
    await send_message(message, hello_msg)
    await bot.send_sticker(message.from_user.id, sticker=br.HELLO_STICKER)
    await send_message(message, f'{br.HELP_MSG}\n{br.COMPANYS_INFO}', kb=k.help_kb())
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    await send_message(message, f'{br.HELP_MSG}\n{br.COMPANYS_INFO}', kb=k.help_kb())
    await message.delete()


@dp.message_handler(commands=['description'])
async def description(message: types.Message):
    desc_msg = br.DESCRIPTION
    await send_message(message, desc_msg)
    await message.delete()


@dp.message_handler(commands=['analytics'])
async def analytics(message: types.Message):
    if market_beat:
        reply = market_beat.get_analysis()
    else:
        reply = br.TYPE_IN
    await send_message(message, reply)
    await message.delete()


@dp.message_handler(commands=['sustainability'])
async def sustainability(message: types.Message):
    if market_beat:
        reply = market_beat.get_sustainability()
    else:
        reply = br.TYPE_IN
    await send_message(message, reply)
    await message.delete()


@dp.message_handler(commands=['dividend'])
async def dividend(message: types.Message):
    if market_beat:
        reply = market_beat.get_dividend()
    else:
        reply = br.TYPE_IN
    await send_message(message, reply)
    await message.delete()


@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    if market_beat:
        reply = market_beat.get_about()
    else:
        reply = br.TYPE_IN
    if len(reply) < MAX_LEN:
        await send_message(message, reply)
        await message.delete()
    else:
        await send_message(message, reply[:MAX_LEN])
        await send_message(message, reply[MAX_LEN:])
        await message.delete()


@dp.message_handler(commands=['chart'])
async def chart(message: types.Message):
    if market_beat:
        url = market_beat.get_chart()
        await message.answer(text='TradingView Chart:',
                             reply_markup=k.chart_kb(url))
    else:
        reply = br.TYPE_IN
        await send_message(message, reply)

    await message.delete()


@dp.message_handler(content_types=['text'])
async def get_info(message: types.Message):
    ticker = message.text.strip().upper()
    if ticker not in tickers_list:
        await message.reply(text=br.SEARCH)
        reply = search_company.search_word(ticker)
        if reply:
            return await send_message(message, br.CHOOSE + reply[0], kb=k.tickers_kb(reply[1]))
        return await send_message(message, '⚠️'+ticker+br.NO_COMP_FOUND)

    global market_beat
    market_beat = bs.MarketBeatInfo(ticker)
    reply = f'<b>Company:</b>\n{market_beat.get_name()}'
    await bot.send_photo(chat_id=message.chat.id,
                         photo=market_beat.get_picture())
    await send_message(message, reply, kb=ReplyKeyboardRemove())
    await send_message(message, br.COMPANYS_INFO, kb=k.actions_kb())


@dp.callback_query_handler()
async def callback_tickers(callback: types.CallbackQuery):
    if callback.data:
        ticker = callback.data
    global market_beat
    market_beat = bs.MarketBeatInfo(ticker)
    reply = f'<b>Company:</b>\n{market_beat.get_name()}'
    await bot.send_photo(chat_id=callback.message.chat.id,
                         photo=market_beat.get_picture())
    await send_message(callback.message, reply, kb=ReplyKeyboardRemove())
    await send_message(callback.message, br.COMPANYS_INFO, kb=k.actions_kb())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
