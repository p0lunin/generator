import random

# ln - максимальная длина дополнительных слов
# k - в процентах, насколько слова не совпадают по буквам
#
class Comparator:
    def __init__(self, k, ln):
        self.k = k
        self.ln = ln

    def compare(self, first, second):
        s = 0
        j = 0
        if abs(len(first) - len(second)) > self.ln:
            return False
        for i in range(len(first)):
            if first[i] in second[j:]:
                s += 1
                j = i
        if len(first) == 0 or s/len(first) > self.k:
            return True
        return False


example = [
    {
        'k': ['a', 'b'],
        'v': 'c'
    }
]


class MessagesComparator:
    def __init__(self, words: list, k1=0.8, k2=0.7, ln=2, ln2=0):
        self.words = words
        self.comp_words = Comparator(k1, ln=ln)
        self.ln2 = ln2
        self.k2 = k2

    def check(self, string: str):
        answers = []
        for sentence in string.lower().split('.'):
            sentence = sentence.replace('\n', ' ').lower()
            for dictt in self.words:
                rule_words = dictt['k']
                answ = dictt['v']
                words_len = len(sentence.split())
                if abs(words_len - len(rule_words)) > self.ln2:
                    continue
                count_eq_words = 0
                i = 0
                for word in sentence.split():
                    try:
                        is_equal = self.comp_words.compare(rule_words[i].lower(), word)
                    except:
                        break
                    if is_equal:
                        count_eq_words += 1
                        i += 1
                if count_eq_words == 0:
                    continue
                if count_eq_words/words_len > self.k2:
                    from_user = dictt.get('from')
                    if from_user:
                        answers.append(f'Как сказал бы <b>{from_user}</b>, <i>{answ}</i>')
                    else:
                        answers.append(answ)
        try:
            return random.choice(answers)
        except:
            return None

    def add_trigger(self, trigger, answer, from_user=None):
        trigger = trigger.split()
        self.words.append({'k': trigger, 'v': answer, 'from': from_user})
