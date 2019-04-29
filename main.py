import random
from telebot import TeleBot, types
from pymongo import MongoClient
from generator import Generator
from rules import RuleGenerator


rul_gen = RuleGenerator()
rul_gen.add_rule('$start')
rul_gen.add_words('$start', ['Я', 'Ты', 'Он', 'Брит', 'Пасюк', 'Двач', 'Гоша', 'Женя'])
rul_gen.add_next('$start', '$action')
rul_gen.add_rule('$action')
rul_gen.add_words('$action', ['хочет', 'не хочет', 'продал', 'полюбил', 'трахнул', 'показал'])
rul_gen.add_next('$action', '$whom')
rul_gen.add_rule('$whom')
rul_gen.add_words('$whom', ['осла', 'крысу', 'двач', 'жопу', 'пасюка', 'меня', 'гошу', 'брита'])
rul_gen.add_next('$whom', '$end_of_mes$')


gen = {}

creator = 268486177
bot = TeleBot('616926239:AAEfQVr4_2tf58Gcok-3YKO1vz6qUHYziVU')
client = MongoClient('mongodb+srv://interbellum_bot:9ga6kKAhm3zAQmp@cluster0-rnman.gcp.mongodb.net/test?retryWrites=true')
db = client.god_db
chats = db.chats
ans_to_appeal = {
    0: ['Согласен с тобой', 'Если вновь такое задумаешь, покараю тебя', 'Не согласен', 'Подумай хорошенько', 'Да ты чертов гений!', 'Зачем я тебя создал, ничтожество...'],
    1: ['Ты это про меня, смертный?', 'Подумай еще раз, и скажи мне это в лицо', 'Холоп несчастный, не видать тебе моих денег как своей женщины'],
    2: ['Опять ты за свое', 'Угомонись уже', 'Не думаю']
}

for chat in chats.find({}):
    gen[chat['id']] = Generator()
    gen[chat['id']].d = chat['words']


def create_gen(chat_id):
    if chat_id not in gen:
        gen[chat_id] = Generator()
        gen[chat_id].add('Я - великий и могучий Перели. Склонись передо мной.')
        chats.insert_one({'id': chat_id, 'words': {}})


@bot.message_handler(commands=['test'])
def story(m):
    bot.delete_message(m.chat.id, m.message_id)
    create_gen(m.chat.id)
    mes = gen[m.chat.id].random_mes()
    if mes:
        bot.send_message(m.chat.id, mes)
    else:
        bot.send_message(m.chat.id, 'Ишь чего захотел. Перехочешь.')


@bot.message_handler(commands=['rul'])
def rul(m):
    bot.delete_message(m.chat.id, m.message_id)
    tts = rul_gen.generate('$start')
    ttt = tts.split(' ')
    if ttt[0] == 'Двач' or ttt[0] == 'Женя':
        if ttt[1] != 'хочет' or ttt[1] != 'не хочет':
            alala = 'а'
            tts = ttt[0] + ' ' + ttt[1] + alala + ' ' + ttt[2]
    bot.send_message(m.chat.id, tts)


@bot.message_handler(commands=['upddb'])
def upd_db(m):
    if m.from_user.id == creator:
        bot.send_message(m.chat.id, 'Начинаю обновление базы данных...')
        for chat_id in gen:
            chats.update_one({'id': chat_id}, {'$set': {'words': gen[chat_id].d}})
        bot.send_message(m.chat.id, 'Обновление успешно!')


@bot.message_handler()
def all_msg(m):
    create_gen(m.chat.id)
    m.text = m.text.lower()
    is_appeal, pos = is_appeal_in_mes(m.text)
    if 'что, если' in m.text:
        bot.send_message(m.chat.id, 'Не будет денег у тебя, вот что')
    elif 'пасюк' in m.text:
        bot.send_message(m.chat.id, 'Лошадкин - мой. Только я его могу его анал трогать.')
    elif is_appeal:
        bot.send_message(m.chat.id, random.choice(ans_to_appeal[pos]))
    if m.text:
        gen[m.chat.id].add(m.text)


appeals = ['бог', 'всевышн', 'перели', 'бож']
def is_appeal_in_mes(text):
    text = text.lower()
    print(text)
    start_appeal = -1
    for appeal in appeals:
        start_appeal = text.find(appeal)
        if start_appeal != -1:
            break
    if start_appeal == -1:
        return False, -1
    strlen = len(text)
    if start_appeal < 20:
        return True, 0
    if start_appeal < strlen/100*80:
        return True, 1
    return True, 2


bot.delete_webhook()
bot.polling(none_stop=True, timeout=600)
