import random
from telebot import TeleBot, types
from rules import *
import googleapiclient.discovery as ds
import time
import pymongo

creator = 268486177
bot = TeleBot('1022401847:AAFiXT966dNxcztL_Bw8lwFHtAe_Sa9DDvE')

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
youtube = ds.build('youtube', 'v3', developerKey='AIzaSyDDvaLsMyPuwr6hWHmIeOMxwc52W4gyrpM')

mongo_client = pymongo.MongoClient('mongodb+srv://bpl_ball:DiMon_2002@cluster0-siw3u.mongodb.net/test?retryWrites=true&w=majority')
bot_db = mongo_client.get_database('bpl_ball')
triggers_col = bot_db.get_collection('triggers')

print('connected to db')


def collection_to_mes_comp():
    triggers_doc = triggers_col.find_one({'id': 0}, {'id': 0, '_id': 0})
    triggers = triggers_doc['triggers']
    for trigger in triggers:
        trigger['k'] = trigger['k'].split()
    print('triggers are:\n', triggers)
    return MessagesComparator(triggers)


triggers = collection_to_mes_comp()
print('triggers are red')


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
def check_not_sova(m):
    print(f'get message "{m.text}"')
    s = 0
    for char in m.text:
        if char in ['y', 'Y', 'u', 'U', 'у', 'У']:
            s += 1
    if s/len(m.text) > 0.5 and len(m.text) > 5:
        try:
            bot.restrict_chat_member(m.chat.id, m.from_user.id, int(time.time())+60)
        except:
            bot.send_message(m.chat.id, '<a href="tg://user?id={}">Ебаклак</a>, убери сову. НЕНАВИЖУ БЛЯТЬ СОВ ЕБАНЫХ'.format(
                                 m.from_user.id), parse_mode='HTML')
        else:
            bot.send_message(m.chat.id,
                             'Забанил <a href="tg://user?id={}">ебаклака</a> за сову. НЕНАВИЖУ БЛЯТЬ СОВ ЕБАНЫХ'.format(
                                 m.from_user.id), parse_mode='HTML')
        try:
            bot.delete_message(m.chat.id, m.message_id)
        except:
            pass
    answ = triggers.check(m.text)
    if answ:
        bot.send_message(m.chat.id, answ, reply_to_message_id=m.message_id)
    if m.reply_to_message:
        keys = m.reply_to_message.text.split('.')
        value = m.text
        for key in keys:
            triggers_col.update_one({'id': 0}, {'$push': {'triggers': {'k': key, 'v': value}}})
            triggers.add_trigger(key, value)
            print(f'new trigger!\nkey:{key}\nvalue:{value}')


bot.polling(none_stop=True, timeout=600)
