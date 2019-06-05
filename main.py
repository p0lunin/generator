import random
import traceback
import requests
from bs4 import BeautifulSoup
from telebot import TeleBot, types
from rules import *
from urllib.parse import unquote
import googleapiclient.discovery as ds
import time

creator = 268486177
bot = TeleBot('616926239:AAG4j5if1vFODOdcqeM9ID8PFCfRyu95kaM')


@bot.message_handler(commands=['test'])
def tst(m):
    bot.send_message(m.chat.id, datetime.datetime.now() + datetime.timedelta(minutes=1, hours=3))


@bot.message_handler(commands=['g'])
def google(m):
    text = m.text.split(' ', maxsplit=1)
    if len(text) != 2:
        bot.send_message(m.chat.id, '/g <запрос>')
        return
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'}
    r = requests.get('http://google.com/search?q={}'.format(text[1]), headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    try:
        items = soup.find_all('div', {'class': 'g'}, limit=5)
    except:
        bot.send_message(m.chat.id, 'Ответов на ваш запрос нет')
        return
    text = 'status-code: {}\n'.format(r.status_code)
    is_ans = False
    for item in items:
        try:
            link = unquote(item.find('h3', {'class': 'r'}).find('a').get('href')[7:])
            pos = link.find('&sa')
            if pos != -1:
                link = link[:pos]
            txt = item.find('h3', {'class': 'r'}).find('a').text
            desc = item.find('span', {'class': 'st'}).text
            desc = desc.replace('<', '&lt;')
            desc = desc.replace('>', '&gt;')
            text += '<a href="{}">{}</a>\n' \
                    '{}\n\n'.format(link, txt, desc)
            is_ans = True
        except:
            continue
    if r.status_code == 429:
        bot.send_message(m.chat.id, 'Гугл посчитал Бога роботом. Пойду ему акции в цене понижу.')
        return
    bot.send_message(m.chat.id, text, parse_mode='HTML', disable_web_page_preview=True)


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
youtube = ds.build('youtube', 'v3', developerKey='AIzaSyDDvaLsMyPuwr6hWHmIeOMxwc52W4gyrpM')


@bot.message_handler(commands=['y'])
def search_youtube(m):
    text = m.text.split(' ', maxsplit=1)
    if len(text) != 2:
        bot.send_message(m.chat.id, '/y <запрос>')
        return
    request = youtube.search().list(
        part='snippet',
        maxResults=5,
        q=text[1]
    )
    response = request.execute()
    text = ''
    print(response)
    if response['pageInfo']['totalResults'] == 0:
        bot.send_message(m.chat.id, 'По вашему запросу ничего не найдено :(')
        return
    for item in response['items']:
        try:
            text += '<a href="http://youtu.be/{}">{}</a>\n'.format(item['id']['videoId'], item['snippet']['title'])
        except KeyError as e:
            text += '<a href="http://youtu.be/{}">{}</a>\n'.format(item['id']['channelId'], item['snippet']['title'])
        text += '{}\n\n'.format(item['snippet']['description'])
    bot.send_message(m.chat.id, text, parse_mode='HTML', disable_web_page_preview=True)


answers = {
    'work': ['Работящий ты наш', 'Работай, че', 'Ебаклак?', 'Я вижу'],
    'who': ['Ты', 'Пасюк', 'Брит', 'Гоша', 'Очко осла', 'Ебаклак', 'Бог', 'Пошел нахуй, заебал',
            'Писос вонючий ебаного осла'],
    'god': ['Да да я'],
    'go dota': ['Я с вами!', 'Ебланы конченные?', '@p0lunin это бан', 'Привет гей']
}


@bot.message_handler(content_types=['text'])
def handler(m):
    s = 0
    for char in m.text:
        if char in ['y', 'Y', 'u', 'U', 'у', 'У']:
            s += 1
    if s/len(m.text) > 0.5 and len(m.text) > 5:
        bot.restrict_chat_member(m.chat.id, m.from_user.id, int(time.time())+60)
        bot.delete_message(m.chat.id, m.message_id)
        bot.send_message(m.chat.id, 'Забанил <a href="tg://user?id={}">ебаклака</a> за сову. НЕНАВИЖУ БЛЯТЬ СОВ ЕБАНЫХ'.format(m.from_user.id), parse_mode='HTML')
    if time_rule.find(m.text):
        bot.send_message(m.chat.id, str(time.ctime()))
    for rule in rules:
        if rules[rule].find(m.text):
            bot.send_message(m.chat.id, random.choice(answers[rule]))
            return


bot.polling(none_stop=True, timeout=600)
