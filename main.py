import telebot
import bs
import search_company
from config import API_KEY

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])

def start(message):
    hello_msg = f'Hello, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    bot.send_message(message.chat.id, hello_msg, parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Im an investment bot', parse_mode='html')

@bot.message_handler(content_types=['text'])
def get_info(message):
    ticker = message.text.strip().lower()
    market_beat = bs.MarketBeatInfo(ticker)
    try:
        reply = market_beat.get_analisys()
        bot.send_message(message.chat.id, reply, parse_mode='html')
    except:
        reply = search_company.search_word(ticker)
        reply = '\n'.join([' -> '.join(t) for t in reply])
        bot.send_message(message.chat.id, reply, parse_mode='html')





bot.polling(non_stop=True)