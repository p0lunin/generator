import random
import traceback
import requests
from bs4 import BeautifulSoup
from telebot import TeleBot, types
from rules import Rule, r
from urllib.parse import unquote
import googleapiclient.discovery as ds
import google_auth_oauthlib.flow as fl

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
    if not is_ans:
        bot.send_message(m.chat.id, 'Ответов на ваш запрос нет')
        return
    bot.send_message(m.chat.id, text, parse_mode='HTML', disable_web_page_preview=True)


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
# flow = fl.InstalledAppFlow.from_client_secrets_file('telegram-bot-12ab15b21c08.json', scopes)
# credentials = flow.run_console()
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


@bot.message_handler(content_types=['text'])
def handler(m):
    is_want_work = r.find(m.text)
    if is_want_work:
        bot.reply_to(m, 'Ты хочешь работать, я вижу!')


bot.polling(none_stop=True, timeout=600)
