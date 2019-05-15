import random
import traceback
from telebot import TeleBot, types
from rules import Rule, r

creator = 268486177
bot = TeleBot('616926239:AAG4j5if1vFODOdcqeM9ID8PFCfRyu95kaM')


@bot.message_handler(content_types=['text'])
def handler(m):
    is_want_work = r.find(m.text)
    if is_want_work:
        bot.reply_to(m, 'Ты хочешь работать, я вижу!')


bot.polling(none_stop=True, timeout=600)
