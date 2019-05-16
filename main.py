import random
import traceback
import requests
from bs4 import BeautifulSoup
from telebot import TeleBot, types
from rules import Rule, r

creator = 268486177
bot = TeleBot('616926239:AAG4j5if1vFODOdcqeM9ID8PFCfRyu95kaM')


@bot.message_handler(commands=['g'])
def google(m):
    text = m.text.split(' ', maxsplit=1)
    if len(text) != 2:
        bot.send_message(m.chat.id, '/g <запрос>')
        return
    r = requests.get('http://google.com/search?q={}'.format(text[1]))
    soup = BeautifulSoup(r.text, features="lxml")
    try:
        items = soup.find_all('div', {'class': 'g'}, limit=5)
    except:
        bot.send_message(m.chat.id, 'Ответов на ваш запрос нет')
        return
    text = ''
    is_ans = False
    for item in items:
        try:
            link = item.find('h3', {'class': 'r'}).find('a').get('href')[7:]
            txt = item.find('h3', {'class': 'r'}).find('a').text
            desc = item.find('span', {'class': 'st'}).text
            desc = desc.replace('<', '&lt;')
            desc = desc.replace('>', '&gt;')
            text += '<a href="{}">{}</a>\n' \
                    '{}\n\n'.format(link, txt, desc)
            is_ans = True
        except:
            continue
    if not is_ans:
        bot.send_message(m.chat.id, 'Ответов на ваш запрос нет')
        return
    print(text)
    bot.send_message(m.chat.id, text, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def handler(m):
    is_want_work = r.find(m.text)
    if is_want_work:
        bot.reply_to(m, 'Ты хочешь работать, я вижу!')


bot.polling(none_stop=True, timeout=600)
