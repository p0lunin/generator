import random
from telebot import TeleBot, types


class Generator:
    def __init__(self):
        self.d = {}
        self.signs_end_of_sent = ['.', '!', '?']

    def add(self, leks):
        if ":START:" in leks or ":END_OF_MES:" in leks or ":END:" in leks:
            return False
        leks = ":START: " + leks
        while leks[-1] in self.signs_end_of_sent:
            leks = leks[:-1]
        leks = leks.replace("\n", " :END_OF_MES: ")
        leks += " :END_OF_MES:"
        for sign in self.signs_end_of_sent:
            leks = leks.replace(sign, ' :END: :START: ')
        leks = leks.split()
        for i in range(len(leks)-1):
            if leks[i] not in self.d.keys():
                self.d[leks[i]] = {}
            if leks[i+1] not in self.d[leks[i]].keys():
                self.d[leks[i]][leks[i + 1]] = 1
            else:
                self.d[leks[i]][leks[i + 1]] += 1
        return True

    def generate(self, first_word):
        try:
            self.d[first_word]
        except:
            return "Unknown word", False
        res = ""
        while True:
            max_num = sum(self.d[first_word].values())
            words = []
            for key, value in self.d[first_word].items():
                temp = [key, value]
                words.append(temp)
            num = random.randint(1, max_num)
            temp = 0
            for word, count in words:
                temp += count
                if num <= temp:
                    if word == ":END_OF_MES:":
                        return res.replace(' :END: :START:', '.')
                    res += word + ' '
                    first_word = word
                    break

    def random_mes(self):
        res = self.generate(':START:')
        while not res:
            res = self.generate(random.choice(list(self.d.keys())))
        return res

gen = {}

bot = TeleBot('616926239:AAEfQVr4_2tf58Gcok-3YKO1vz6qUHYziVU')


def create_gen(chat_id):
    if not chat_id in gen:
        gen[chat_id] = Generator()
        gen[chat_id].add('Я - великий и могучий Перели. Склонись передо мной.') 


@bot.message_handler(commands=['test'])
def story(m):
    create_gen(m.chat.id)
    mes = gen[m.chat.id].random_mes()
    if mes:
        bot.send_message(m.chat.id, mes)
    else:
        bot.send_message(m.chat.id, 'Ишь чего захотел. Перехочешь.')


@bot.message_handler(commands=['print'])
def pr(m):
    print(gen[m.chat_id].d)
    bot.send_message(m.chat.id, 'ok')


@bot.message_handler()
def all_msg(m):
    create_gen(m.chat.id)
    if m.text:
        gen[m.chat.id].add(m.text)


bot.delete_webhook()
bot.polling(none_stop=True, timeout=600)
