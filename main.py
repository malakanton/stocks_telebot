from aiogram import Bot, executor, Dispatcher, types
import bs
import search_company
from config import API_KEY
import bots_replies as br

with open('tickers_list.txt', 'r') as f:
    tickers_list = f.readline().split()

bot = Bot(API_KEY)
dp = Dispatcher(bot)

market_beat = None


def send_message(message: types.Message, text:str):
    return message.answer(text=text, parse_mode='html')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    hello_msg = f'Hello, <b>{message.from_user.first_name} {message.from_user.last_name}</b>!\n{br.TYPE_IN}'
    await send_message(message, hello_msg)
    await message.delete()


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await send_message(message, br.HELP_MSG)
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


@dp.message_handler(content_types=['text'])
async def get_info(message: types.Message):
    ticker = message.text.strip().upper()
    if ticker not in tickers_list:
        await send_message(message, br.SEARCH)
        reply = search_company.search_word(ticker)
        if reply:
            await send_message(message, br.CHOOSE + reply)
        else:
            await send_message(message, ticker+br.NO_COMP_FOUND)
        return

    global market_beat
    market_beat = bs.MarketBeatInfo(ticker)
    reply = f'Company:\n{market_beat.get_name()}'
    await send_message(message, reply)
    await send_message(message, br.COMPANYS_INFO)


@dp.message_handler(commands=['analytics'])
async def analytics(message: types.Message):
    reply = market_beat.get_analysis()
    await send_message(message, reply)
    await message.delete()


@dp.message_handler(commands=['sustainability'])
async def sustainability(message: types.Message):
    reply = market_beat.get_sustainability()
    await send_message(message, reply)
    await message.delete()

# reply = market_beat.get_analisys()
# bot.send_message(message.chat.id, reply, parse_mode='html')



if __name__ == '__main__':
    executor.start_polling(dp)
