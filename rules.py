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
        if s/len(first) > self.k:
            return True
        return False


class Rule:
    def __init__(self, rule, words, k1=0.8, k2=3, ln=2):
        """
        :param rule: str in format "keyword keyword keyword3"
        :param words: dict in format {keyword: [word1, word2], keyword2: [word1, word2]}
        """
        self.words = words
        self.rule = rule.lower().split()
        self.len_rule = len(self.rule)
        self.comp = Comparator(k1, ln=ln)
        self.k2 = k2

    def find(self, string):
        l = string.lower().split()
        now_check = 0
        i = -1
        for word in l:
            for keyword in self.words[self.rule[now_check]]:
                if self.comp.compare(keyword, word):
                    now_check += 1
                    i = -1
                    if now_check == self.len_rule:
                        return True
                    break
            if now_check != 0:
                i += 1
            if i == self.k2:
                return False
        return False


rules = {
    'work': Rule('i want work', {'i': ['я', 'мне', 'меня'], 'want': ['хочу', 'хочется', 'желаю', 'желание'], 'work': ['работать', 'пахать', 'вкалывать', 'подметать', 'чистить']}),
    'who': Rule('who', {'who': ['кто']}, k1=0.75),
    'god': Rule('god', {'god': ['бог', 'боже', 'господь']}, k1=0.7)
}
